from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
from pydantic import BaseModel
import uuid
import asyncio
from app.services.jules_client import get_jules_client
from app.services.orchestrator import OrchestratorEngine
from app.models.api import RunWorkflowRequest, WorkflowResponse

from app.routes.agents import AGENTS_DIR
import os

from app.database import get_db_pool, json_safe
import json

router = APIRouter()

@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(request: RunWorkflowRequest):
    """Starts a new autonomous workflow chain entirely driven by the filesystem."""
    run_id = str(uuid.uuid4())
    
    # Check if the repo is initialized with the .jao folder.
    # If not, override the starting agent to @onboard to bootstrap it.
    is_init = await OrchestratorEngine.is_repo_initialized(request.github_repo_id)
    if not is_init:
        starting_agent = "syncer_onboard"
        task = "Initialize .jao directory, task board, and project map."
    else:
        # Fall back to reading the blackboard if no agent is specified
        next_step = await OrchestratorEngine.read_blackboard_state(request.github_repo_id)
        if next_step:
            starting_agent = next_step["next_agent"]
            task = next_step["prompt"]
        else:
            return {"error": "No uncompleted tasks assigned on the blackboard."}

    # Insert initial state into DB
    pool = get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO workflow_runs (run_id, status, current_agent, task, history)
            VALUES ($1::uuid, $2, $3, $4, $5)
            """,
            run_id, "STARTING", starting_agent, task, "[]"
        )
    
    # Fire and forget the infinite loop
    asyncio.create_task(_run_engine_loop(run_id, starting_agent, task, request))
    
    return WorkflowResponse(
        session_id=run_id,
        status="RUNNING",
        message=f"Autonomous Blackboard Workflow started with {starting_agent}"
    )

@router.get("/{run_id}")
async def get_workflow_status(run_id: str):
    # (Unchanged)
    pool = get_db_pool()
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            """
            SELECT status, current_agent, task, history
            FROM workflow_runs
            WHERE run_id = $1::uuid
            """,
            run_id
        )
        if not record:
            return {"error": "Not found"}

        state = dict(record)
        if state.get("history") and isinstance(state["history"], str):
             state["history"] = json.loads(state["history"])
        return json_safe(state)


def _read_file_sync(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def _run_engine_loop(run_id: str, start_agent: str, start_task: str, request: RunWorkflowRequest):
    """
    The Autonomous Filesystem Loop (Virtual Firm Edition).
    It reads the `.jao/` directory state, spawns the assigned agent,
    waits for them to complete, deletes the session, and repeats.
    """
    client = get_jules_client()
    pool = get_db_pool()
    
    current_agent = start_agent
    current_prompt = start_task
    
    while current_agent:
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workflow_runs SET status = $1, current_agent = $2 WHERE run_id = $3::uuid",
                f"AGENT_ACTIVE: {current_agent}", current_agent, run_id
            )
        
        # 1. Load the persona from the .md file securely
        try:
            safe_agent = os.path.basename(current_agent)
            if safe_agent != current_agent or ".." in current_agent:
                raise ValueError("Invalid agent identifier.")

            persona_path = os.path.join(AGENTS_DIR, f"{safe_agent}.md")
            if not os.path.exists(persona_path):
                persona_path = os.path.join(AGENTS_DIR, "audit_agents", f"{safe_agent}.md")

            abs_persona_path = os.path.abspath(persona_path)
            abs_agents_dir = os.path.abspath(AGENTS_DIR)

            if not abs_persona_path.startswith(abs_agents_dir + os.sep):
                raise ValueError("Path traversal attempt detected.")
            
            persona_content = await asyncio.to_thread(_read_file_sync, abs_persona_path)
        except Exception as e:
            logger.exception("Error loading persona: %s", e)
            persona_content = "Error loading persona."
            
        # 2. Inject the entire Blackboard State (.jao/) into the prompt so the agent isn't blind
        system_context = await OrchestratorEngine.get_context_injection(request.github_repo_id)
        
        full_prompt = f"IDENTITY:\n{persona_content}\n\n{system_context}\n\nASSIGNED TASK:\n{current_prompt}"

        # 3. Create the Session
        session = await client.create_session(
            prompt=full_prompt,
            source=request.github_repo_id,
            title=f"JAO: {current_agent} run",
            require_plan_approval=request.interactive
        )
        
        session_id = session.get("id")
        if not session_id or "error" in session:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE workflow_runs SET status = $1 WHERE run_id = $2::uuid",
                    f"ERROR: {session.get('error', 'Failed to create session')}", run_id
                )
            break
            
        # Optional: Auto-approve plans if we want true zero-touch autonomy
        if request.interactive:
            await client.approve_plan(session_id)
            
        # 4. Wait for the agent to finish modifying the repository and `.jao/` folders
        timeout_counter = 0
        max_iterations = 360  # Allow up to ~30 minutes

        while timeout_counter < max_iterations:
            activities = await client.list_activities(session_id)
            is_done = any(a.get("status") in ["completed", "failed"] for a in activities)
            if is_done:
                break
            timeout_counter += 1
            await asyncio.sleep(5)
            
        if timeout_counter >= max_iterations:
            logger.error(f"Session {session_id} timed out after 30 minutes.")

        # 5. Clean up: Delete the session to keep Jules memory/resources clean.
        await client.delete_session(session_id)

        # Log completion
        new_history_entry = {
            "agent": current_agent,
            "session_id": session_id,
            "status": "COMPLETED_AND_CLEARED" if timeout_counter < max_iterations else "TIMED_OUT"
        }

        async with pool.acquire() as conn:
             record = await conn.fetchrow("SELECT history FROM workflow_runs WHERE run_id = $1::uuid", run_id)
             if record:
                 history_str = record["history"] or "[]"
                 history = json.loads(history_str) if isinstance(history_str, str) else history_str
                 if isinstance(history, str):
                      history = json.loads(history)
                 history.append(new_history_entry)
                 await conn.execute(
                     "UPDATE workflow_runs SET history = $1 WHERE run_id = $2::uuid",
                     json.dumps(history), run_id
                 )
        
        # 6. Parse for the next agent by reading `.jao/task_board.md` again
        if timeout_counter >= max_iterations:
            break

        next_step = await OrchestratorEngine.read_blackboard_state(request.github_repo_id)
        
        if next_step:
            current_agent = next_step["next_agent"]
            current_prompt = next_step["prompt"]
            request.interactive = (next_step["mode"] == "Interactive Plan")
        else:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE workflow_runs SET status = $1, current_agent = NULL WHERE run_id = $2::uuid",
                    "COMPLETED_FIRM_WORKFLOW", run_id
                )
            break

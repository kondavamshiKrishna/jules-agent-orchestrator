from fastapi import APIRouter
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
    """Starts a new workflow chain"""
    run_id = str(uuid.uuid4())
    
    # Insert initial state into DB
    pool = get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO workflow_runs (run_id, status, current_agent, task, history)
            VALUES ($1::uuid, $2, $3, $4, $5)
            """,
            run_id, "STARTING", request.starting_agent, request.task, "[]"
        )
    
    # We don't await this so the UI gets a fast response
    asyncio.create_task(_run_engine_loop(run_id, request))
    
    return WorkflowResponse(
        session_id=run_id,
        status="RUNNING",
        message=f"Workflow started with {request.starting_agent}"
    )

@router.get("/{run_id}")
async def get_workflow_status(run_id: str):
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

        # Need to deserialize JSONB string back to dict/list
        state = dict(record)
        if state.get("history") and isinstance(state["history"], str):
             state["history"] = json.loads(state["history"])
        return json_safe(state)

async def _run_engine_loop(run_id: str, request: RunWorkflowRequest):
    """The infinite loop described in the architecture plan"""
    client = get_jules_client()
    pool = get_db_pool()
    
    # Loop variables
    current_agent = request.starting_agent
    current_prompt = f"USER TASK: {request.task}"
    retry_count = 0
    MAX_RETRIES = 2
    
    while current_agent:
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workflow_runs SET status = $1, current_agent = $2 WHERE run_id = $3::uuid",
                f"AGENT_ACTIVE: {current_agent}", current_agent, run_id
            )
        
        # 1. Load the persona from the .md file
        try:
            persona_path = os.path.join(AGENTS_DIR, f"{current_agent}.md")
            if not os.path.exists(persona_path):
                # Check audit_agents folder
                persona_path = os.path.join(AGENTS_DIR, "audit_agents", f"{current_agent}.md")
            
            with open(persona_path, "r", encoding="utf-8") as f:
                persona_content = f.read()
        except Exception as e:
            persona_content = f"Error loading persona: {e}"
            
        # In multi-agent systems, agents MUST know what happened before.
        # We need to inject the context/history of the previous steps
        # otherwise they lose track of the assignment context.
        previous_history = ""
        async with pool.acquire() as conn:
            record = await conn.fetchrow("SELECT history FROM workflow_runs WHERE run_id = $1::uuid", run_id)
            if record and record["history"]:
                try:
                    hist_arr = json.loads(record["history"]) if isinstance(record["history"], str) else record["history"]
                    if isinstance(hist_arr, str): hist_arr = json.loads(hist_arr)
                    if hist_arr:
                        # Grab the last output to provide context
                        last_output = hist_arr[-1].get("output", "")
                        previous_history = f"\n\nPREVIOUS STEP CONTEXT:\n{last_output}\n"
                except Exception:
                    pass

        full_prompt = f"IDENTITY:\n{persona_content}\n\nTASK:\n{current_prompt}{previous_history}"
        
        # 2. Create the session
        session = client.create_session(
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
            
        # 3. If it's Interactive Mode, approve the plan automatically (for demo)
        if request.interactive:
            client.approve_plan(session_id)
            
        # 4. Poll for activities and completion
        final_output = ""
        timeout_counter = 0
        while True:
            # Prevent infinite hang. Assumes 1 hour max (720 * 5s)
            if timeout_counter > 720:
                 final_output = "ERROR: Timeout waiting for agent to finish."
                 break
            timeout_counter += 1

            # Re-fetch from DB if we need robust resume/kill checking.
            # For now, just poll Jules
            activities = client.list_activities(session_id)
            
            if activities:
                text_activities = [a for a in activities if a.get("type") == "message" and a.get("role") == "assistant"]
                if text_activities:
                    final_output = text_activities[-1].get("text", "")
            
            # Robust completion check:
            # In a real SDK, we'd check `client.sessions.get(session_id).status == 'COMPLETED'`
            # Or look for an explicit end marker.
            # For this alpha mock, checking if the session activity list explicitly marks 'completed' status.
            is_done = any(a.get("status") in ["completed", "failed", "error"] for a in activities)

            # Additional heuristic: If no new activities for a long time and last was text.
            # (In reality, we'd rely on the SDK's explicit state).
            if is_done:
                break
                
            await asyncio.sleep(5)
            
        # Log to history
        new_history_entry = {
            "agent": current_agent,
            "session_id": session_id,
            "output": final_output
        }

        async with pool.acquire() as conn:
             # Fetch current history, append, and update.
             record = await conn.fetchrow("SELECT history FROM workflow_runs WHERE run_id = $1::uuid", run_id)
             if record:
                 history_str = record["history"] or "[]"
                 history = json.loads(history_str) if isinstance(history_str, str) else history_str
                 if isinstance(history, str):
                      history = json.loads(history) # parse again if it was double stringified
                 history.append(new_history_entry)
                 await conn.execute(
                     "UPDATE workflow_runs SET history = $1 WHERE run_id = $2::uuid",
                     json.dumps(history), run_id
                 )
        
        # 5. Parse for the next agent
        next_step = OrchestratorEngine.parse_handover(final_output)
        
        if next_step and next_step.get("status") == "STALLED_NO_HANDOVER":
             if retry_count < MAX_RETRIES:
                 retry_count += 1
                 current_prompt = "ERROR: You failed to provide the correct handover formatting. Please resend your output and explicitly assign the next step using the required format (e.g. 'Assigned to: @tag' or 'How to Verify (for @tina):' or 'TASK COMPLETE')."
                 # Keep current_agent the same so they retry
             else:
                 async with pool.acquire() as conn:
                    await conn.execute(
                        "UPDATE workflow_runs SET status = $1, current_agent = NULL WHERE run_id = $2::uuid",
                        "ERROR: STALLED_NO_HANDOVER_LIMIT_REACHED", run_id
                    )
                 break
        elif next_step and next_step.get("next_agent"):
            retry_count = 0 # reset on successful handoff
            current_agent = next_step["next_agent"]
            current_prompt = next_step["prompt"]
            request.interactive = (next_step["mode"] == "Interactive Plan")
        else:
            status = next_step.get("status", "COMPLETED") if next_step else "COMPLETED"
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE workflow_runs SET status = $1, current_agent = NULL WHERE run_id = $2::uuid",
                    status, run_id
                )
            break

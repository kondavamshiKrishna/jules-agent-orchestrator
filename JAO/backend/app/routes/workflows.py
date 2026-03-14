from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import asyncio
from app.services.jules_client import get_jules_client
from app.services.orchestrator import OrchestratorEngine
from app.models.api import RunWorkflowRequest, WorkflowResponse

from app.routes.agents import AGENTS_DIR
import os

router = APIRouter()

# In-memory store for demo. Phase 2: Move to SQLite
active_workflows = {}

@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(request: RunWorkflowRequest):
    """Starts a new workflow chain"""
    run_id = str(uuid.uuid4())
    
    # Initialize state
    active_workflows[run_id] = {
        "status": "STARTING",
        "current_agent": request.starting_agent,
        "task": request.task,
        "history": []
    }
    
    # We don't await this so the UI gets a fast response
    asyncio.create_task(_run_engine_loop(run_id, request))
    
    return WorkflowResponse(
        session_id=run_id,
        status="RUNNING",
        message=f"Workflow started with {request.starting_agent}"
    )

@router.get("/{run_id}")
async def get_workflow_status(run_id: str):
    if run_id not in active_workflows:
        return {"error": "Not found"}
    return active_workflows[run_id]

async def _run_engine_loop(run_id: str, request: RunWorkflowRequest):
    """The infinite loop described in the architecture plan"""
    client = get_jules_client()
    state = active_workflows[run_id]
    
    # Loop variables
    current_agent = request.starting_agent
    current_prompt = f"USER TASK: {request.task}"
    
    while current_agent:
        state["status"] = f"AGENT_ACTIVE: {current_agent}"
        
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
            
        full_prompt = f"IDENTITY:\n{persona_content}\n\nTASK:\n{current_prompt}"
        
        # 2. Create the session
        session = await asyncio.to_thread(
            client.create_session,
            prompt=full_prompt,
            source=request.github_repo_id,
            title=f"JAO: {current_agent} run",
            require_plan_approval=request.interactive
        )
        
        session_id = session.get("id")
        if not session_id or "error" in session:
            state["status"] = f"ERROR: {session.get('error', 'Failed to create session')}"
            break
            
        # 3. If it's Interactive Mode, approve the plan automatically (for demo)
        if request.interactive:
            await asyncio.to_thread(client.approve_plan, session_id)
            
        # 4. Poll for activities and completion
        final_output = ""
        while True:
            activities = await asyncio.to_thread(client.list_activities, session_id)
            # Find the most recent activity that marks completion or output
            # In Jules, completion often means the agent has stopped writing or specific metadata.
            # For this MVP, we look for 'COMPLETED' status or final message.
            # Real SDK might have a 'wait_for_completion' or activity status 'AGENT_PROCESS_DONE'
            
            # Simple polling logic:
            if activities:
                # Let's assume the last activity with text is the output
                text_activities = [a for a in activities if a.get("type") == "message" and a.get("role") == "assistant"]
                if text_activities:
                    final_output = text_activities[-1].get("text", "")
            
            # Check if session is done (this would depend on SDK activity types)
            # Placeholder: Check if any activity has 'status': 'completed'
            is_done = any(a.get("status") == "completed" for a in activities)
            if is_done:
                break
                
            await asyncio.sleep(5)
            
        # Log to history
        state["history"].append({
            "agent": current_agent,
            "session_id": session_id,
            "output": final_output
        })
        
        # 5. Parse for the next agent
        next_step = OrchestratorEngine.parse_handover(final_output)
        
        if next_step:
            current_agent = next_step["next_agent"]
            current_prompt = next_step["prompt"]
            request.interactive = (next_step["mode"] == "Interactive Plan")
        else:
            state["status"] = "COMPLETED"
            break

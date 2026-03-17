from pydantic import BaseModel
from typing import List, Optional

class RunWorkflowRequest(BaseModel):
    task: str
    starting_agent: str
    github_repo_id: str
    interactive: bool = True
    plan: str = "free"

class WorkflowResponse(BaseModel):
    session_id: str
    status: str
    message: str

class AgentPersona(BaseModel):
    id: str
    name: str
    description: str
    file_path: str

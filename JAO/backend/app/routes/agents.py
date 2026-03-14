import os
import glob
from fastapi import APIRouter
from app.models.api import AgentPersona
from typing import List

router = APIRouter()

# Assuming the backend is inside JAO/backend, the agents are two levels up
<<<<<<< HEAD

AGENTS_DIR = os.getenv("AGENTS_DIR")
if not AGENTS_DIR:
    # Check if /jewels_agents exists (Docker path)
    if os.path.exists("/jewels_agents"):
        AGENTS_DIR = "/jewels_agents"
    else:
        # Fallback to local path
        AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

=======
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
>>>>>>> origin/main
AUDIT_AGENTS_DIR = os.path.join(AGENTS_DIR, "audit_agents")

@router.get("/", response_model=List[AgentPersona])
def list_agents():
    """Reads all .md files in the jewels_agents directory and returns them as available personas."""
    personas = []
    
    # Read main agents
    main_files = glob.glob(os.path.join(AGENTS_DIR, "*.md"))
    for file_path in main_files:
        filename = os.path.basename(file_path)
        if filename == "MASTER_PLAN.md":
            continue
            
        personas.append(AgentPersona(
            id=filename.replace(".md", ""),
            name=filename.replace(".md", "").replace("_", " ").title(),
            description=f"Core agent: {filename}",
            file_path=file_path
        ))
        
    # Read audit agents
    audit_files = glob.glob(os.path.join(AUDIT_AGENTS_DIR, "*.md"))
    for file_path in audit_files:
        filename = os.path.basename(file_path)
        personas.append(AgentPersona(
            id=filename.replace(".md", ""),
            name=filename.replace(".md", "").replace("_", " ").title(),
            description=f"Audit agent: {filename}",
            file_path=file_path
        ))
        
    return personas

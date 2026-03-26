import os
import glob
from fastapi import APIRouter
from app.models.api import AgentPersona
from typing import List
from functools import lru_cache

router = APIRouter()

# Assuming the backend is inside JAO/backend, the agents are two levels up
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
AUDIT_AGENTS_DIR = os.path.join(AGENTS_DIR, "audit_agents")


def _load_personas_from_dir(
    directory: str, description_prefix: str, exclude_files: List[str] = None
) -> List[AgentPersona]:
    """Helper to load AgentPersonas from markdown files in a given directory."""
    exclude_set = set(exclude_files) if exclude_files else set()

    personas = []
    file_paths = glob.glob(os.path.join(directory, "*.md"))
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        if filename in exclude_set:
            continue

        personas.append(
            AgentPersona(
                id=filename.replace(".md", ""),
                name=filename.replace(".md", "").replace("_", " ").title(),
                description=f"{description_prefix}: {filename}",
                file_path=file_path,
            )
        )
    return personas


@lru_cache(maxsize=1)
def get_all_agents() -> List[AgentPersona]:
    personas = []

    # Read main agents
    personas.extend(
        _load_personas_from_dir(
            AGENTS_DIR, "Core agent", exclude_files=["MASTER_PLAN.md"]
        )
    )

    # Read audit agents
    personas.extend(_load_personas_from_dir(AUDIT_AGENTS_DIR, "Audit agent"))

    return personas


@router.get("/", response_model=List[AgentPersona])
def list_agents():
    """Reads all .md files in the jewels_agents directory and returns them as available personas."""
    return get_all_agents()

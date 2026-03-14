import re

with open('JAO/backend/app/routes/agents.py', 'r') as f:
    content = f.read()

replacement = """
from functools import lru_cache

@lru_cache(maxsize=1)
def _get_agent_personas() -> List[AgentPersona]:
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

@router.get("/", response_model=List[AgentPersona])
def list_agents():
    \"\"\"Reads all .md files in the jewels_agents directory and returns them as available personas.\"\"\"
    return _get_agent_personas()
"""

# Replace the list_agents function
import sys
if "def list_agents():" in content:
    # use regex to replace from @router.get to the end
    content = re.sub(r'@router\.get\("/", response_model=List\[AgentPersona\]\)\ndef list_agents\(\):.*?return personas\n', replacement.strip() + '\n', content, flags=re.DOTALL)

    with open('JAO/backend/app/routes/agents.py', 'w') as f:
        f.write(content)
else:
    print("Could not find list_agents")

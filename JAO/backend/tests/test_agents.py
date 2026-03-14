import pytest
from app.routes.agents import (
    _load_personas_from_dir,
    list_agents,
    AGENTS_DIR,
    AUDIT_AGENTS_DIR,
)
import os
import glob
from unittest.mock import patch, MagicMock


# Let's mock the AgentPersona creation since it's just inheriting from a mock BaseModel in the tests
class MockAgentPersona:
    def __init__(self, id, name, description, file_path):
        self.id = id
        self.name = name
        self.description = description
        self.file_path = file_path


@patch("app.routes.agents.AgentPersona", MockAgentPersona)
@patch("app.routes.agents.glob.glob")
def test_load_personas_from_dir(mock_glob):
    # Mock some markdown files being returned by glob
    mock_glob.return_value = [
        "/path/to/agent1.md",
        "/path/to/agent_two.md",
        "/path/to/MASTER_PLAN.md",
    ]

    # Test without exclusions
    personas = _load_personas_from_dir("/path/to", "Prefix")
    assert len(personas) == 3
    assert personas[0].id == "agent1"
    assert personas[0].name == "Agent1"
    assert personas[0].description == "Prefix: agent1.md"
    assert personas[0].file_path == "/path/to/agent1.md"

    assert personas[1].id == "agent_two"
    assert personas[1].name == "Agent Two"
    assert personas[1].description == "Prefix: agent_two.md"

    # Test with exclusions
    personas = _load_personas_from_dir(
        "/path/to", "Prefix", exclude_files=["MASTER_PLAN.md"]
    )
    assert len(personas) == 2
    ids = [p.id for p in personas]
    assert "agent1" in ids
    assert "agent_two" in ids
    assert "MASTER_PLAN" not in ids


@patch("app.routes.agents.AgentPersona", MockAgentPersona)
@patch("app.routes.agents._load_personas_from_dir")
def test_list_agents(mock_load):
    # Mock the return values of _load_personas_from_dir
    mock_load.side_effect = [
        [
            MockAgentPersona(
                id="core1", name="Core1", description="desc", file_path="path"
            )
        ],
        [
            MockAgentPersona(
                id="audit1", name="Audit1", description="desc", file_path="path"
            )
        ],
    ]

    personas = list_agents()

    assert len(personas) == 2
    assert personas[0].id == "core1"
    assert personas[1].id == "audit1"

    # Check that _load_personas_from_dir was called twice with correct arguments
    assert mock_load.call_count == 2
    mock_load.assert_any_call(
        AGENTS_DIR, "Core agent", exclude_files=["MASTER_PLAN.md"]
    )
    mock_load.assert_any_call(AUDIT_AGENTS_DIR, "Audit agent")

import pytest
from app.services.orchestrator import OrchestratorEngine

def test_parse_handover_priya():
    text = "Handover for @Priya: Please create a plan for the new feature."
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "priya_promptcraft",
        "prompt": "Please create a plan for the new feature.",
        "mode": "Interactive Plan"
    }

def test_parse_handover_priya_with_tag():
    text = "@priya, review this architecture\n---"
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "priya_promptcraft",
        "prompt": "review this architecture",
        "mode": "Interactive Plan"
    }

def test_parse_handover_assignment_pydan():
    text = """
    Assigned to: Daniel (@pydan)
    Prompt for @pydan: Implement the login endpoint.
    """
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "py_dan_backend",
        "prompt": "Implement the login endpoint.",
        "mode": "Interactive Plan"
    }

def test_parse_handover_assignment_tina():
    text = """
    Assigned to: Tina (@tina)
    Full Prompt for @tina: Write tests for the login endpoint.
    ---
    """
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "test_tina_qa",
        "prompt": "Write tests for the login endpoint.",
        "mode": "Start"
    }

def test_parse_handover_tina_verify():
    text = "How to Verify (for @tina): Test the new endpoint with pytest."
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "test_tina_qa",
        "prompt": "Test the new endpoint with pytest.",
        "mode": "Start"
    }

def test_parse_handover_tina_test():
    text = "How to Test (for @tina): Use mock data for testing.\n---"
    result = OrchestratorEngine.parse_handover(text)
    assert result == {
        "next_agent": "test_tina_qa",
        "prompt": "Use mock data for testing.",
        "mode": "Start"
    }

def test_parse_handover_none():
    text = "This is a random output without any handovers."
    result = OrchestratorEngine.parse_handover(text)
    assert result is None

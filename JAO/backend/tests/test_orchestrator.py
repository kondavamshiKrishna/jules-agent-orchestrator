import pytest
import os
import asyncio
from unittest.mock import patch, mock_open
from app.services.orchestrator import OrchestratorEngine

def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapper

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

class TestOrchestratorEngineV2:
    @async_test
    async def test_fetch_remote_file_error_path(self):
        """Verify that an exception during local file read returns None and logs the error."""
        test_exception = Exception("Disk Error")
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", side_effect=test_exception):
                with patch("app.services.orchestrator.logger.error") as mock_logger:
                    result = await OrchestratorEngine.fetch_remote_file("test-repo", ".jao/task_board.md")
                    assert result is None
                    mock_logger.assert_called_once_with("Failed to read local file %s: %s", ".jao/task_board.md", "Exception")

    @async_test
    async def test_fetch_remote_file_success(self):
        """Verify successful local file read."""
        content = "test content"
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=content)):
                result = await OrchestratorEngine.fetch_remote_file("test-repo", ".jao/task_board.md")
                assert result == content

    @async_test
    async def test_is_repo_initialized(self):
        """Verify initialization check based on task board existence."""
        with patch.object(OrchestratorEngine, "fetch_remote_file") as mock_fetch:
            # Case 1: Initialized
            mock_fetch.return_value = "board content"
            assert await OrchestratorEngine.is_repo_initialized("test-repo") is True

            # Case 2: Not initialized
            mock_fetch.return_value = None
            assert await OrchestratorEngine.is_repo_initialized("test-repo") is False

    @async_test
    async def test_read_blackboard_state_bootstrap(self):
        """Verify bootstrap state when task board is missing."""
        with patch.object(OrchestratorEngine, "fetch_remote_file", return_value=None):
            result = await OrchestratorEngine.read_blackboard_state("test-repo")
            assert result["next_agent"] == "syncer_onboard"
            assert "Initialize" in result["prompt"]

    @async_test
    async def test_read_blackboard_state_task_assigned(self):
        """Verify task assignment logic."""
        board_content = "- [ ] Implement the backend (Assigned to: @pydan)"
        with patch.object(OrchestratorEngine, "fetch_remote_file", return_value=board_content):
            result = await OrchestratorEngine.read_blackboard_state("test-repo")
            assert result["next_agent"] == "py_dan_backend"
            assert result["mode"] == "Start"
            assert "Implement the backend" in result["prompt"]

    @async_test
    async def test_read_blackboard_state_no_uncompleted_tasks(self):
        """Verify None is returned when all tasks are complete."""
        board_content = "- [x] Finished task (@pydan)"
        with patch.object(OrchestratorEngine, "fetch_remote_file", return_value=board_content):
            result = await OrchestratorEngine.read_blackboard_state("test-repo")
            assert result is None

    @async_test
    async def test_get_context_injection(self):
        """Verify context injection string assembly."""
        map_content = "Project Map Details"
        board_content = "Task Board Details"

        async def mock_fetch_file(repo, path):
            if path == ".jao/project_map.md":
                return map_content
            if path == ".jao/task_board.md":
                return board_content
            return None

        with patch.object(OrchestratorEngine, "fetch_remote_file", side_effect=mock_fetch_file):
            context = await OrchestratorEngine.get_context_injection("test-repo")
            assert "=== JAO REPOSITORY STATE ===" in context
            assert map_content in context
            assert board_content in context

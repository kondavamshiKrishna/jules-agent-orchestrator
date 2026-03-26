import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import uuid

# Define a mock class for RunWorkflowRequest since the mocked Pydantic in conftest
# breaks the default constructor.
class MockRunWorkflowRequest:
    def __init__(self, task, starting_agent, github_repo_id, interactive=True):
        self.task = task
        self.starting_agent = starting_agent
        self.github_repo_id = github_repo_id
        self.interactive = interactive

# Mock WorkflowResponse since the real one inherits from mocked BaseModel
class MockWorkflowResponse:
    def __init__(self, session_id, status, message):
        self.session_id = session_id
        self.status = status
        self.message = message

def async_test(f):
    def wrapper(*args, **kwargs):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapper

@patch("app.routes.workflows.WorkflowResponse", MockWorkflowResponse)
@patch("app.models.api.WorkflowResponse", MockWorkflowResponse)
@patch("app.routes.workflows.get_db_pool")
@patch("app.routes.workflows.OrchestratorEngine.check_and_read_blackboard", new_callable=AsyncMock)
@patch("app.routes.workflows._run_engine_loop")
@patch("app.routes.workflows.asyncio.create_task")
@async_test
async def test_run_workflow_not_initialized(mock_create_task, mock_run_loop, mock_check_and_read_blackboard, mock_get_db_pool):
    mock_check_and_read_blackboard.return_value = (False, None)

    # Setup mock db pool
    mock_conn = AsyncMock()
    mock_pool = MagicMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_get_db_pool.return_value = mock_pool

    request = MockRunWorkflowRequest(task="dummy", starting_agent="dummy", github_repo_id="repo123")

    # We must import inside the function to ensure patches take effect
    from app.routes.workflows import run_workflow
    response = await run_workflow(request)

    assert response.status == "RUNNING"
    assert "syncer_onboard" in response.message

    mock_check_and_read_blackboard.assert_called_once_with("repo123")

    # Assert DB call
    mock_conn.execute.assert_called_once()
    args, kwargs = mock_conn.execute.call_args
    assert "INSERT INTO workflow_runs" in args[0]
    assert args[2] == "STARTING"
    assert args[3] == "syncer_onboard"
    assert args[4] == "Initialize .jao directory, task board, and project map."

    mock_create_task.assert_called_once()
    mock_run_loop.assert_called_once()

@patch("app.routes.workflows.WorkflowResponse", MockWorkflowResponse)
@patch("app.models.api.WorkflowResponse", MockWorkflowResponse)
@patch("app.routes.workflows.get_db_pool")
@patch("app.routes.workflows.OrchestratorEngine.check_and_read_blackboard", new_callable=AsyncMock)
@patch("app.routes.workflows._run_engine_loop")
@patch("app.routes.workflows.asyncio.create_task")
@async_test
async def test_run_workflow_initialized_with_task(mock_create_task, mock_run_loop, mock_check_and_read_blackboard, mock_get_db_pool):
    mock_check_and_read_blackboard.return_value = (True, {"next_agent": "priya_promptcraft", "prompt": "Test prompt", "mode": "Autonomous"})

    # Setup mock db pool
    mock_conn = AsyncMock()
    mock_pool = MagicMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_get_db_pool.return_value = mock_pool

    request = MockRunWorkflowRequest(task="dummy", starting_agent="dummy", github_repo_id="repo123")

    from app.routes.workflows import run_workflow
    response = await run_workflow(request)

    assert response.status == "RUNNING"
    assert "priya_promptcraft" in response.message

    mock_check_and_read_blackboard.assert_called_once_with("repo123")

    # Assert DB call
    mock_conn.execute.assert_called_once()
    args, kwargs = mock_conn.execute.call_args
    assert args[3] == "priya_promptcraft"
    assert args[4] == "Test prompt"

    mock_create_task.assert_called_once()
    mock_run_loop.assert_called_once()

@patch("app.routes.workflows.WorkflowResponse", MockWorkflowResponse)
@patch("app.models.api.WorkflowResponse", MockWorkflowResponse)
@patch("app.routes.workflows.get_db_pool")
@patch("app.routes.workflows.OrchestratorEngine.check_and_read_blackboard", new_callable=AsyncMock)
@patch("app.routes.workflows._run_engine_loop")
@patch("app.routes.workflows.asyncio.create_task")
@async_test
async def test_run_workflow_initialized_no_task(mock_create_task, mock_run_loop, mock_check_and_read_blackboard, mock_get_db_pool):
    mock_check_and_read_blackboard.return_value = (True, None)

    request = MockRunWorkflowRequest(task="dummy", starting_agent="dummy", github_repo_id="repo123")

    from app.routes.workflows import run_workflow
    response = await run_workflow(request)

    assert type(response) is dict
    assert "error" in response
    assert response["error"] == "No uncompleted tasks assigned on the project blackboard."

    mock_check_and_read_blackboard.assert_called_once_with("repo123")
    mock_get_db_pool.assert_not_called()
    mock_create_task.assert_not_called()

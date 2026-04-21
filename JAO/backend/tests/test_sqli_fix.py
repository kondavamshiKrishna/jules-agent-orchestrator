import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.routes.workflows import _run_engine_loop

class MockRunWorkflowRequest:
    def __init__(self):
        self.github_repo_id = "test_repo"
        self.interactive = False

def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

@async_test
async def test_sqli_fix_parameters():
    run_id = "00000000-0000-0000-0000-000000000000"
    current_agent = "attacker' --"
    request = MockRunWorkflowRequest()

    from unittest.mock import patch
    with patch("app.routes.workflows.get_db_pool") as mock_db_pool, \
         patch("app.routes.workflows.get_jules_client") as mock_jules_client, \
         patch("app.routes.workflows.OrchestratorEngine") as mock_engine:

        mock_conn = AsyncMock()
        mock_acquire = MagicMock()
        mock_acquire.__aenter__.return_value = mock_conn
        mock_db_pool.return_value.acquire.return_value = mock_acquire

        mock_engine.get_context_injection = AsyncMock(return_value="Mocked context")
        mock_engine.read_blackboard_state = AsyncMock(return_value=None)

        mock_conn.fetchrow.return_value = {"history": "[]"}

        mock_client = AsyncMock()
        mock_jules_client.return_value = mock_client
        mock_client.create_session.return_value = {"id": "test_session"}
        mock_client.list_activities.return_value = [{"status": "completed"}]

        await _run_engine_loop(run_id, current_agent, "task", request)

        # Check the first UPDATE call
        update_calls = [call for call in mock_conn.execute.mock_calls if "UPDATE workflow_runs SET status = 'AGENT_ACTIVE: ' || $1" in str(call)]
        assert len(update_calls) > 0

        sql, arg1, arg2 = update_calls[0].args
        assert sql == "UPDATE workflow_runs SET status = 'AGENT_ACTIVE: ' || $1, current_agent = $1 WHERE run_id = $2::uuid"
        assert arg1 == current_agent
        assert arg2 == run_id

@async_test
async def test_sqli_fix_error_parameters():
    run_id = "00000000-0000-0000-0000-000000000000"
    current_agent = "test_agent"
    request = MockRunWorkflowRequest()

    from unittest.mock import patch
    with patch("app.routes.workflows.get_db_pool") as mock_db_pool, \
         patch("app.routes.workflows.get_jules_client") as mock_jules_client, \
         patch("app.routes.workflows.OrchestratorEngine") as mock_engine:

        mock_conn = AsyncMock()
        mock_acquire = MagicMock()
        mock_acquire.__aenter__.return_value = mock_conn
        mock_db_pool.return_value.acquire.return_value = mock_acquire

        mock_engine.get_context_injection = AsyncMock(return_value="Mocked context")
        mock_engine.read_blackboard_state = AsyncMock(return_value=None)

        mock_client = AsyncMock()
        mock_jules_client.return_value = mock_client
        # Simulate error in session creation
        mock_client.create_session.return_value = {"error": "injection' --"}

        await _run_engine_loop(run_id, current_agent, "task", request)

        # Check the error UPDATE call
        update_calls = [call for call in mock_conn.execute.mock_calls if "UPDATE workflow_runs SET status = 'ERROR: ' || $1" in str(call)]
        assert len(update_calls) > 0

        sql, arg1, arg2 = update_calls[0].args
        assert sql == "UPDATE workflow_runs SET status = 'ERROR: ' || $1 WHERE run_id = $2::uuid"
        assert arg1 == "injection' --"
        assert arg2 == run_id

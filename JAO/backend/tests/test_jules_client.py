import pytest
from unittest.mock import patch, MagicMock
import jules_agent_sdk

# Ensure JulesClient exists in the mocked module so it can be patched
if not hasattr(jules_agent_sdk, 'JulesClient'):
    jules_agent_sdk.JulesClient = MagicMock()

from app.services.jules_client import JulesService
from jules_agent_sdk.exceptions import JulesAPIError

def async_test(f):
    def wrapper(*args, **kwargs):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            pass
    return wrapper

@async_test
async def test_create_session_success():
    with patch('jules_agent_sdk.JulesClient') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.sessions.create.return_value = {"id": "session-123", "status": "ACTIVE"}

        service = JulesService(api_key="test-key")
        result = await service.create_session(
            prompt="test prompt",
            source="test source",
            title="test title",
            require_plan_approval=True
        )

        assert result == {"id": "session-123", "status": "ACTIVE"}
        mock_instance.sessions.create.assert_called_once_with(
            prompt="test prompt",
            source="test source",
            title="test title",
            require_plan_approval=True
        )

@async_test
async def test_create_session_api_error():
    with patch('jules_agent_sdk.JulesClient') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.sessions.create.side_effect = JulesAPIError("API error occurred")

        service = JulesService(api_key="test-key")
        result = await service.create_session(
            prompt="test prompt",
            source="test source",
            title="test title",
            require_plan_approval=True
        )

        assert isinstance(result, dict)
        assert result["error"] == "API error occurred"

@async_test
async def test_create_session_no_client():
    # Force self.client to be None by making the constructor raise an exception
    with patch('jules_agent_sdk.JulesClient', side_effect=Exception("Failed to load")):
        service = JulesService(api_key="test-key")
        assert service.client is None

        result = await service.create_session(
            prompt="test prompt",
            source="test source",
            title="test title",
            require_plan_approval=True
        )

        assert result == {"id": "dummy_session_id", "status": "ACTIVE"}

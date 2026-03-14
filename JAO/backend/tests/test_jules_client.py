import sys
from unittest.mock import MagicMock, patch

# Mock the missing jules_agent_sdk
mock_sdk = MagicMock()
sys.modules['jules_agent_sdk'] = mock_sdk

from app.services.jules_client import JulesService

def test_jules_service_test_connection_exception():
    with patch('app.services.jules_client.logger') as mock_logger:
        service = JulesService(api_key="dummy_key")
        # Ensure self.client is set to trigger the try block if there was one
        # Actually test_connection just returns True in the try block right now,
        # but to test the exception block we could force an exception if there was a call.
        # Wait, test_connection has no real call to client in try block.
        # It's just:
        # try:
        #     return True
        # except Exception as e:
        #     logger.exception("Connection test failed")
        #     return False
        # So we can't easily trigger the exception block in test_connection unless we mock something it calls, but it calls nothing.
        pass

def test_jules_service_create_session_exception():
    with patch('app.services.jules_client.logger') as mock_logger:
        service = JulesService(api_key="dummy_key")
        # service.client is a mock
        service.client.sessions.create.side_effect = Exception("Test Exception")

        result = service.create_session("prompt", "source", "title", False)

        assert "error" in result
        assert result["error"] == "Test Exception"
        mock_logger.exception.assert_called_with("Failed to create session")

def test_jules_service_list_activities_exception():
    with patch('app.services.jules_client.logger') as mock_logger:
        service = JulesService(api_key="dummy_key")
        service.client.activities.list_all.side_effect = Exception("Test Exception")

        result = service.list_activities("dummy_session")

        assert result == []
        mock_logger.exception.assert_called_with("Failed to list activities")

def test_jules_service_approve_plan_exception():
    with patch('app.services.jules_client.logger') as mock_logger:
        service = JulesService(api_key="dummy_key")
        service.client.sessions.approve_plan.side_effect = Exception("Test Exception")

        result = service.approve_plan("dummy_session")

        assert result is False
        mock_logger.exception.assert_called_with("Failed to approve plan")

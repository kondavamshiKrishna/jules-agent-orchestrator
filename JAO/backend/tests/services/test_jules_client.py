import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from app.services.jules_client import JulesService
try:
    from jules_agent_sdk.exceptions import JulesAPIError
except ImportError:
    JulesAPIError = Exception

def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapper

def test_jules_service_test_connection_no_client():
    service = JulesService("dummy")
    service.client = None
    assert service.test_connection() is False

def test_jules_service_test_connection_success():
    service = JulesService("dummy")
    service.client = MagicMock()
    assert service.test_connection() is True

def test_jules_service_test_connection_failure():
    service = JulesService("dummy")
    service.client = MagicMock()
    service.client.sources.list.side_effect = JulesAPIError("API Error")
    assert service.test_connection() is False

@async_test
async def test_jules_service_list_activities_no_client():
    service = JulesService("dummy")
    service.client = None
    activities = await service.list_activities("session_123")
    assert activities == []

@async_test
async def test_jules_service_list_activities_success():
    service = JulesService("dummy")
    service.client = MagicMock()
    mock_activities = [{"id": "act_1", "type": "message"}]
    service.client.activities.list_all.return_value = mock_activities

    activities = await service.list_activities("session_123")
    assert activities == mock_activities
    service.client.activities.list_all.assert_called_once_with("session_123")

@async_test
async def test_jules_service_list_activities_failure():
    service = JulesService("dummy")
    service.client = MagicMock()
    service.client.activities.list_all.side_effect = JulesAPIError("API Error")

    activities = await service.list_activities("session_123")
    assert activities == []

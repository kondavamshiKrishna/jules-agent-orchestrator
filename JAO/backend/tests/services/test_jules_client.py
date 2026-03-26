import pytest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from app.services.jules_client import JulesService
try:
    from jules_agent_sdk.exceptions import JulesAPIError
except ImportError:
    JulesAPIError = Exception

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

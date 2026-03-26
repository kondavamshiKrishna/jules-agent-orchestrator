import pytest
from unittest.mock import MagicMock, patch

# Need to set up environment so that imports work
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.services.jules_client import JulesService

def test_jules_service_test_connection_no_client():
    # Arrange
    service = JulesService("dummy_api_key")
    service.client = None

    # Act
    result = service.test_connection()

    # Assert
    assert result is False

def test_jules_service_test_connection_success():
    # Arrange
    service = JulesService("dummy_api_key")
    service.client = MagicMock()

    # Act
    result = service.test_connection()

    # Assert
    assert result is True

def test_jules_service_test_connection_no_client_mocked():
    # Arrange
    service = JulesService("dummy_api_key")
    # Simulate failed SDK instantiation
    service.client = None

    # Act
    result = service.test_connection()

    # Assert
    assert result is False

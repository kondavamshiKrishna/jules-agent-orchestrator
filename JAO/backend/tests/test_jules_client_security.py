import pytest
import os
from unittest.mock import patch
from app.services.jules_client import get_jules_client, JulesService
import app.services.jules_client as jules_client

def test_get_jules_client_raises_error_if_key_missing():
    """
    Test that the implementation now raises a ValueError when JULES_API_KEY is missing.
    """
    # Reset the global state for the test
    jules_client.active_jules_client = None

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as excinfo:
            get_jules_client()
        assert "JULES_API_KEY environment variable is not set." in str(excinfo.value)

def test_get_jules_client_with_env_var():
    """
    Test that the implementation correctly uses the JULES_API_KEY environment variable.
    """
    # Reset the global state for the test
    jules_client.active_jules_client = None

    with patch.dict(os.environ, {"JULES_API_KEY": "secret_key"}):
        client = get_jules_client()
        assert client.api_key == "secret_key"

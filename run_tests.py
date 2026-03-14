import sys
import unittest.mock
sys.modules['fastapi'] = unittest.mock.MagicMock()
sys.modules['fastapi.middleware.cors'] = unittest.mock.MagicMock()
sys.modules['fastapi.testclient'] = unittest.mock.MagicMock()
sys.modules['pydantic'] = unittest.mock.MagicMock()
sys.modules['jules_agent_sdk'] = unittest.mock.MagicMock()
import pytest
pytest.main(["JAO/backend/tests/"])

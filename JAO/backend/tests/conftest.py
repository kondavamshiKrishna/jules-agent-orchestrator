import sys
from unittest.mock import MagicMock

class MockBaseModel:
    pass

class MockPydantic:
    BaseModel = MockBaseModel

sys.modules['pydantic'] = MockPydantic()
sys.modules['asyncpg'] = MagicMock()
class MockException(Exception): pass
class MockExceptions:
    JulesAPIError = MockException
    JulesAuthenticationError = MockException

class MockJulesAgentSDK:
    exceptions = MockExceptions()

sys.modules['jules_agent_sdk'] = MockJulesAgentSDK()
sys.modules['jules_agent_sdk.exceptions'] = MockExceptions()


class MockResponse:
    def __init__(self, status_code, headers, url=None):
        self.url = url
        self.status_code = status_code
        self.headers = headers
    def json(self):
        return {"status": "healthy"} if self.url == "/health" else {}
    def get(self, key, default=""):
        return self.headers.get(key, default)

class MockTestClient:
    def __init__(self, app):
        self.app = app
    def options(self, url, headers=None, **kwargs):
        headers = headers or {}
        req_method = headers.get("Access-Control-Request-Method", "")
        req_headers = headers.get("Access-Control-Request-Headers", "")
        origin = headers.get("Origin", "")

        # Simulate FastAPI CORS logic
        resp_headers = {}
        if origin == "http://localhost:3005":
            resp_headers["access-control-allow-origin"] = origin
            resp_headers["access-control-allow-methods"] = "GET, POST" if req_method in ["POST", "GET"] else ""
            resp_headers["access-control-allow-headers"] = "Content-Type" if req_headers == "Content-Type" else ""
            return MockResponse(200, resp_headers, url)
        return MockResponse(400, resp_headers, url)

    def get(self, url, headers=None, **kwargs):
        headers = headers or {}
        origin = headers.get("Origin", "")
        resp_headers = {}
        if origin == "http://localhost:3005":
            resp_headers["access-control-allow-origin"] = origin
        return MockResponse(200, resp_headers, url)

class MockFastapiTestClient:
    TestClient = MockTestClient

class MockRouter:
    def get(self, *args, **kwargs):
        def wrapper(f): return f
        return wrapper
    def post(self, *args, **kwargs):
        def wrapper(f): return f
        return wrapper

class MockFastAPIClass:
    def __init__(self, *args, **kwargs):
        pass
    def add_middleware(self, *args, **kwargs):
        pass
    def include_router(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        def wrapper(f): return f
        return wrapper

class MockFastapi:
    FastAPI = MockFastAPIClass
    APIRouter = MockRouter

sys.modules['fastapi.testclient'] = MockFastapiTestClient()
sys.modules['fastapi'] = MockFastapi()
sys.modules['fastapi.middleware'] = MagicMock()
sys.modules['fastapi.middleware.cors'] = MagicMock()

import contextlib
contextlib.asynccontextmanager = lambda f: f

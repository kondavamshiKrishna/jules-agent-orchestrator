from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_cors_preflight_allowed():
    # CORS preflight (OPTIONS)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3005",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3005"
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "Content-Type" in response.headers["access-control-allow-headers"]

def test_cors_preflight_method_not_allowed():
    # DELETE should not be allowed
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3005",
            "Access-Control-Request-Method": "DELETE",
        },
    )
    assert "DELETE" not in response.headers.get("access-control-allow-methods", "")

def test_cors_preflight_header_not_allowed():
    # X-Custom-Header should not be allowed
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3005",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-Custom-Header",
        },
    )
    assert "X-Custom-Header" not in response.headers.get("access-control-allow-headers", "")

def test_actual_request_allowed_origin():
    response = client.get("/health", headers={"Origin": "http://localhost:3005"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3005"

def test_actual_request_disallowed_origin():
    response = client.get("/health", headers={"Origin": "http://malicious.com"})
    assert "access-control-allow-origin" not in response.headers

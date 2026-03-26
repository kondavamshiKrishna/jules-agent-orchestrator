import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# We mock asyncpg globally in conftest, but we need Record to be a type.
import asyncpg
if getattr(asyncpg, "Record", None) is None or not isinstance(asyncpg.Record, type):
    asyncpg.Record = type('Record', (dict,), {})

from app.routes.workflows import get_workflow_status

# In the backend testing environment, pytest-asyncio markers may not work natively.
# Asynchronous tests should use a custom wrapper/decorator (e.g., async_test) that
# manually retrieves the event loop and uses loop.run_until_complete() to execute
# async def test functions.
def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

@async_test
@patch("app.routes.workflows.get_db_pool")
async def test_get_workflow_status_found(mock_get_db_pool):
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_get_db_pool.return_value = mock_pool

    mock_conn.fetchrow.return_value = asyncpg.Record({
        "status": "RUNNING",
        "current_agent": "py_dan_backend",
        "task": "do something",
        "history": '[{"agent": "py_dan_backend", "status": "COMPLETED"}]'
    })

    result = await get_workflow_status("123e4567-e89b-12d3-a456-426614174000")

    assert result["status"] == "RUNNING"
    assert result["current_agent"] == "py_dan_backend"
    assert result["task"] == "do something"
    assert result["history"] == [{"agent": "py_dan_backend", "status": "COMPLETED"}]

@async_test
@patch("app.routes.workflows.get_db_pool")
async def test_get_workflow_status_not_found(mock_get_db_pool):
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_get_db_pool.return_value = mock_pool

    mock_conn.fetchrow.return_value = None

    result = await get_workflow_status("123e4567-e89b-12d3-a456-426614174000")

    assert result == {"error": "Not found"}

@async_test
@patch("app.routes.workflows.get_db_pool")
async def test_get_workflow_status_history_not_string(mock_get_db_pool):
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
    mock_get_db_pool.return_value = mock_pool

    mock_conn.fetchrow.return_value = asyncpg.Record({
        "status": "COMPLETED",
        "current_agent": None,
        "task": "do something",
        "history": [{"agent": "py_dan_backend", "status": "COMPLETED"}]
    })

    result = await get_workflow_status("123e4567-e89b-12d3-a456-426614174000")

    assert result["history"] == [{"agent": "py_dan_backend", "status": "COMPLETED"}]

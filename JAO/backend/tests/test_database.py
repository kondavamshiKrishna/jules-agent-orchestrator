import datetime
from decimal import Decimal
from uuid import uuid4
import pytest
from unittest.mock import patch

import app.database as db

class MockRecord(dict):
    pass

@pytest.fixture(autouse=True)
def mock_asyncpg_record():
    with patch('app.database.asyncpg.Record', MockRecord):
        yield

def test_json_safe_basic_types():
    assert db.json_safe("string") == "string"
    assert db.json_safe(123) == 123
    assert db.json_safe(12.3) == 12.3
    assert db.json_safe(True) is True
    assert db.json_safe(None) is None

def test_json_safe_list():
    assert db.json_safe([1, "two", 3.0]) == [1, "two", 3.0]
    assert db.json_safe([]) == []

def test_json_safe_dict():
    assert db.json_safe({"a": 1, "b": "two"}) == {"a": 1, "b": "two"}
    assert db.json_safe({}) == {}

def test_json_safe_decimal():
    assert db.json_safe(Decimal('10.5')) == 10.5
    assert db.json_safe(Decimal('0')) == 0.0

def test_json_safe_datetime():
    dt = datetime.datetime(2024, 1, 1, 12, 0, 0)
    assert db.json_safe(dt) == "2024-01-01T12:00:00"

    d = datetime.date(2024, 1, 1)
    assert db.json_safe(d) == "2024-01-01"

def test_json_safe_uuid():
    u = uuid4()
    assert db.json_safe(u) == str(u)

def test_json_safe_asyncpg_record():
    u = uuid4()
    dt = datetime.datetime(2024, 1, 1, 12, 0, 0)
    record = MockRecord({
        "id": u,
        "amount": Decimal("100.50"),
        "created_at": dt,
        "name": "Test"
    })

    safe = db.json_safe(record)
    assert safe == {
        "id": str(u),
        "amount": 100.5,
        "created_at": "2024-01-01T12:00:00",
        "name": "Test"
    }

def test_json_safe_nested():
    u = uuid4()
    dt = datetime.datetime(2024, 1, 1, 12, 0, 0)
    nested = {
        "list": [Decimal("1.1"), Decimal("2.2")],
        "record": MockRecord({"nested_uuid": u}),
        "dict": {"dt": dt}
    }

    safe = db.json_safe(nested)
    assert safe == {
        "list": [1.1, 2.2],
        "record": {"nested_uuid": str(u)},
        "dict": {"dt": "2024-01-01T12:00:00"}
    }

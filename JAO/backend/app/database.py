import asyncpg
import json
from decimal import Decimal

db_pool = None

async def init_db_pool():
    global db_pool
    dsn = "postgresql://jao_user:jao_pass@timescale:5432/jao"

    # First connect to create the schema if it doesn't exist
    try:
        conn = await asyncpg.connect(dsn)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS workflow_runs (
                run_id UUID PRIMARY KEY,
                status VARCHAR(255) NOT NULL,
                current_agent VARCHAR(255),
                task TEXT,
                history JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await conn.close()
    except Exception as e:
        print(f"Warning: Failed to initialize schema automatically: {e}")

    # Then create the pool
    db_pool = await asyncpg.create_pool(dsn=dsn)

async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()

def get_db_pool():
    return db_pool

def json_safe(obj):
    """
    Recursively converts non-serializable objects (like asyncpg.Record, Decimal, UUID)
    into standard Python types for JSON serialization.
    """
    if isinstance(obj, asyncpg.Record):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(i) for i in obj]
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    if hasattr(obj, 'isoformat'): # datetime handling
        return obj.isoformat()
    from uuid import UUID
    if isinstance(obj, UUID):
        return str(obj)
    return obj

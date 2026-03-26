# Note: Ensure 'asyncpg' is installed via winget or pip
import asyncpg
import os
import json
from decimal import Decimal

db_pool = None

async def init_db_pool():
    global db_pool
    # Real app would use env vars for DSN
    db_pool = await asyncpg.create_pool(
        dsn=os.getenv("DATABASE_URL", "postgresql://jao_user:jao_pass@timescale:5432/jao")
    )
    
    # Ensure tables exist
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS workflow_runs (
                run_id UUID PRIMARY KEY,
                status TEXT,
                current_agent TEXT,
                task TEXT,
                history JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


async def init_db_schema():
    global db_pool
    if db_pool:
        async with db_pool.acquire() as conn:
            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS workflow_runs (
                    run_id UUID PRIMARY KEY,
                    status VARCHAR(50),
                    current_agent VARCHAR(100),
                    task TEXT,
                    history JSONB
                )
                '''
            )

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
    if isinstance(obj, (list, tuple, set)):
        return [json_safe(i) for i in obj]
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    # Could handle UUIDs, datetimes here if needed by converting to str
    if hasattr(obj, 'isoformat'): # datetime handling
        return obj.isoformat()
    # UUID handling is usually done gracefully by FastAPI's JSONResponse,
    # but we can force it to str to be safe.
    from uuid import UUID
    if isinstance(obj, UUID):
        return str(obj)
    return obj

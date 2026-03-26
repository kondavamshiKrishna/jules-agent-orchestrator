import asyncio
import asyncpg
import os
import logging

logger = logging.getLogger(__name__)

async def init_db():
    logger.info("Initializing database schema...")
    # Real app would use env vars for DSN
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])

    try:
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

            -- Trigger for updated_at (optional, but good practice)
            CREATE OR REPLACE FUNCTION update_modified_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ language 'plpgsql';

            DROP TRIGGER IF EXISTS update_workflow_runs_modtime ON workflow_runs;

            CREATE TRIGGER update_workflow_runs_modtime
            BEFORE UPDATE ON workflow_runs
            FOR EACH ROW
            EXECUTE FUNCTION update_modified_column();
        """)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.exception("Failed to initialize schema: %s", e)
    finally:
        await conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())

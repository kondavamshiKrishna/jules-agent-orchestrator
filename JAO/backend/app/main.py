import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import workflows, agents
from contextlib import asynccontextmanager
from app.database import init_db_pool, close_db_pool, init_db_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db_pool()
    await init_db_schema()
    yield
    # Shutdown
    await close_db_pool()

app = FastAPI(title="Jules Agent Orchestrator (JAO)", version="0.1.0", lifespan=lifespan)

# Security: Restrict origins in production
# For now, we restrict to the known frontend port
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3005")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])

@app.get("/health")
async def health_check() -> dict:
    """
    Check the health status of the application.
    Returns a dictionary indicating the API is healthy.
    """
    return {"status": "healthy"}

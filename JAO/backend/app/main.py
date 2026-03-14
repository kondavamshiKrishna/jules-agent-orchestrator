from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import workflows, agents

app = FastAPI(title="Jules Agent Orchestrator (JAO)", version="0.1.0")

# Security: Restrict origins in production
# For now, we restrict to the known frontend port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3005"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

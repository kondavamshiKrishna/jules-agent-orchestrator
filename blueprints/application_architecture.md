# Blueprint: Application Architecture (JAO)

## 🏗️ System Overview
The Jules Agent Orchestrator (JAO) is a multi-tier application designed to facilitate autonomous agent interaction with a trading infrastructure.

### 1. Layers
- **Frontend**: React (Vite) + Lucide Icons. Polls the backend for "Activity logs" every 3-5 seconds to show agent progress.
- **Backend API**: FastAPI. Manages the "State Machine" of which agent is currently active.
- **Database**: TimescaleDB (PostgreSQL). Stores activity logs, trade history, and agent session data.
- **The Brain**: External Jules SDK/API. The backend sends tasks to Jules, oriented by the **Live Project Context (LPC)** layer (`.jao/project_map.md`).

## 🔄 Data Flow
1. **User** → Triggers a workflow.
2. **Backend/Syncer** → Creates a "Mission" and updates `.jao/task_board.md`.
3. **Session Genesis** → Jules spawns the agent.
4. **Orientation** → Agent reads `.jao/project_map.md` (Rule 0) to find files.
5. **Execution & Write-Back** → Agent works, updates `.jao/task_board.md`, and assigns the next agent.
6. **Baton Transfer** → Backend/Syncer detects the handoff and spawns the next agent.

## 🔐 Session & Security
- **Simultaneous Sessions**: Handled via UUIDs in the database.
- **Jules API Keys**: Loaded via `.env`.
- **CORS**: Restricts communication to the local Docker network for safety.

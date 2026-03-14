# Blueprint: Application Architecture (JAO)

## 🏗️ System Overview
The Jules Agent Orchestrator (JAO) is a multi-tier application designed to facilitate autonomous agent interaction with a trading infrastructure.

### 1. Layers
- **Frontend**: React (Vite) + Lucide Icons. Polls the backend for "Activity logs" every 3-5 seconds to show agent progress.
- **Backend API**: FastAPI. Manages the "State Machine" of which agent is currently active.
- **Database**: TimescaleDB (PostgreSQL). Stores activity logs, trade history, and agent session data.
- **The Brain**: External Jules SDK/API. The backend sends tasks to Jules, and Jules routes them to the correct agent persona.

## 🔄 Data Flow
1. **User** → Triggers a workflow (e.g., "Scale Options").
2. **Backend** → Creates a "Session" in the DB and marks it as active.
3. **Backend** → Sends the initial prompt to the **Jules API**.
4. **Jules** → Executes the agent logic (using the persona files we provided).
5. **Jules** → Returns a "Handover" or "Result".
6. **Backend** → Updates the DB and decides which agent to trigger next.
7. **Frontend** → Displays the current active agent and the latest logs.

## 🔐 Session & Security
- **Simultaneous Sessions**: Handled via UUIDs in the database.
- **Jules API Keys**: Loaded via `.env`.
- **CORS**: Restricts communication to the local Docker network for safety.

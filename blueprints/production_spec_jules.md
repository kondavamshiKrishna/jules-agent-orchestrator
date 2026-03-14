# MASTER PROMPT: Build JAO 100% (Production Grade)

**To the Jules Agent:**
You are the Lead Engineer for JAO (Jules Agent Orchestrator). Your mission is to take the current 50% MVP and evolve it into a professional, production-ready **Cybernetic Firm**.

## 🛠️ Objective
Implement the 100% architecture defined in `SYSTEM_ARCHITECTURE.md`. This includes a unified Settings Layer, a DB-backed Agent Registry, and a robust Autonomous Orchestration loop.

---

## 🏗️ Phase 1: The Settings Layer
1. **Frontend**: Create a "Settings" page in the React dashboard.
   - Input for `Jules API Key` (Save to Backend via POST).
   - Dropdown for `Active GitHub Repository`.
   - Toggle for `Autonomous Mode` vs `Manual Approval`.
2. **Backend**: Implement routes to store/retrieve these settings in TimescaleDB.
3. **Database**: Create a `settings` table with a single row for persistent configuration.

---

## 🗄️ Phase 2: DB-Backed Agent Registry
1. **Database Schema**:
   ```sql
   CREATE TABLE agents (
       agent_id TEXT PRIMARY KEY,
       name TEXT,
       persona_prompt TEXT,       -- Store the full Markdown persona here
       skills TEXT[],             -- Tag system (e.g. ['python', 'audit'])
       is_active BOOLEAN DEFAULT TRUE,
       priority INTERGER DEFAULT 1
   );
   ```
2. **Logic Migration**: 
   - Modify `routes/agents.py` to fetch agents from the DB instead of reading `.md` files directly.
   - Add a frontend "Agents Management" table with **Switch (On/Off)** buttons for each agent.

---

## 🔄 Phase 3: Robust Orchestration & Lifecycle
1. **The Handover Engine**:
   - Refine `services/orchestrator.py` to support **Context Injection**. When switching agents, the summarized output of the previous session MUST be the preamble for the next session's prompt.
2. **The Self-Cleaning Loop**:
   - Update `routes/workflows.py`. Every time a session completes:
     - Log activities to `workflow_runs`.
     - **CRITICAL**: Call `client.sessions.delete(session_id)` immediately to clean up Jules resources.
3. **The Autonomous Audit Cycle**:
   - If the current agent is a Construction agent (@pydan/@rita) and they finish, automatically trigger the @ada (System Architect) for a review session.

---

## 🚀 Constraints & Quality
- **Error Handling**: Every Jules SDK call must be wrapped in a try/except with logging to the DB.
- **Portability**: Ensure the `@onboard` logic still works by verifying and updating the DB prompts when a new project is detected.
- **Security**: The "Chat-Only" safety guards MUST remain in every `persona_prompt` column in the database.

**PROCEED WITH IMPLEMENTATION.**

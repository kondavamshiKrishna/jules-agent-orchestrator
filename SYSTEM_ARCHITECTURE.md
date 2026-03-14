# 🏗️ JAO: System Architecture & Orchestration Blueprint
**Version**: 1.0.0 (Professional Edition)
**Status**: ACTIVE / AUTONOMOUS

---

## 🏛️ 100% Target Architecture Overview

The Jules Agent Orchestrator (JAO) is a **Cybernetic Firm Infrastructure**. This document serves as the **Target Blueprint**. If the current codebase (50%) does not match this blueprint, it is considered "Feature Pending." The system is designed to grow into this exact structure.

### 🛠️ Core Technology Stack (100% Production Spec)
| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | React 18, Vite, Lucide | **Pro Dashboard**: Management of API keys, Repo selection, and Agent Status switches. |
| **Backend** | FastAPI (Python 3.11) | **Autonomous Hub**: Processes signals, manages DB state, and handles Jules API transactions. |
| **Orchestration** | Signal-Driven State Machine | Parses terminal outputs for `[NEXT_AGENT]` and `[TASK_DONE]` signals. |
| **Database** | TimescaleDB | **Source of Truth**: Stores Prompts, Skills, Activity logs, and Session history. |
| **AI Engine** | Jules SDK | **Compute Layer**: Isolated VMs for each agent session. |

---

## 🔄 The Autonomous Orchestration Loop

The system operates on an **Agent-Native Lifecycle**. Instead of linear execution, it uses a recursive loop where agents check, build, audit, and verify each other.

### 🔄 The "Document-First" Workflow (The Firm's Pulse)
The system no longer relies on volatile chat history. Instead, it uses a **Blackboard Architecture** where the shared filesystem is the source of truth.

1.  **The Trigger**: A user request or a "Brainstorming" cycle initiates a session.
2.  **The Proposal**: `@ada` (Architect) performs research and writes a **`BLUEPRINT.md`** to `JAO/sessions/{id}/inbox/`.
3.  **The Handshake**: The `OrchestratorEngine` detects the file, hashes it, and stores the metadata in the DB.
4.  **The Assignment**: The Orchestrator assigns the next agent (e.g., `@pydan`) and feeds the contents of `BLUEPRINT.md` directly into their system prompt.
5.  **The Implementation**: `@pydan` writes an **`EXECUTION_LOG.md`** and the actual code changes to the repo.
6.  **The Audit**: Auditors read the implementation log to verify against the original blueprint.

### 1. The Decision Engine (Orchestrator)
The `OrchestratorEngine` (in `services/orchestrator.py`) is the "brain" that monitors the field. It performs **Handover Parsing**:
- It scans the output of every completed agent session for standard tags (e.g., `[NEXT_AGENT: @pydan]`).
- It extracts the **Context Payload** (the prompt for the next agent).
- It initiates a "Context Transfer" where the results of the previous work are passed to the next specialist.

### 2. Session Lifecycle & Dynamic Scaling (100% Scope)
- **Simultaneous Session Control**: The Orchestrator tracks a `MAX_AGENTS` constant. If the limit is 5, and 10 tasks are queued, the system maintains a "Waiting Room" in the database.
- **Autonomous Teardown**: As soon as an agent emits a `Done ✅` signal, the Orchestrator immediately:
    1. Synchronizes the VM filesystem with the main repository.
    2. Flushes the ephemeral session memory to the **Global Context Store** in TimescaleDB.
    3. Terminates the Jules VM to reclaim credits/resources.
    4. Automatically spawns the next agent from the queue.

### 3. "The Fielding" & Spare Parts System
We use a **Dynamic Fielder Model**. Agents are treated as interchangeable parts based on their specialization.
-**Initialization Scan**: Before any task, `@onboard` performs a "Ground Check" to verify all agents are mapped to the correct project paths. 
-**Specialized Deployment**: Auditing agents (like `@scalper_auditor`) are "Bench Players." They are only moved to the "Active Field" when a specific module failure is detected.

---

## 📈 Data Flow Diagram (Mermaid)

```mermaid
graph TD
    User((User)) -->|Triggers Workflow| API[FastAPI Orchestrator]
    API -->|Create Session| Jules[Jules SDK / VM]
    Jules -->|Execute Persona| Agent[Active Agent]
    Agent -->|Code Changes| Repo[GitHub / Local Repo]
    Agent -->|Handover Signal| API
    API -->|Parse & Log| DB[(TimescaleDB)]
    DB -->|Read Activity| UI[React Frontend]
    UI -->|Monitor| User
    API -->|Trigger Next| Jules
```

---

## 📡 Jules API Integration Detail

### Function: `create_session`
- **Purpose**: Spawns a dedicated AI instance with a specific persona.
- **Data Flow**: `Backend -> Jules -> VM Initialization`.
- **Functions used**: `client.sessions.create(prompt, source, title, require_plan_approval)`.

### Function: `list_activities`
- **Purpose**: The "Persistence Engine." It pulls every command and terminal output from the agent's VM.
- **Data Flow**: `Jules -> Backend -> TimescaleDB`.
- **Functions used**: `client.activities.list_all(session_id)`.

---

## 🚀 Portability & @onboard Logic
The system is designed to be **Zero-Config Portable**.
1. **Verification**: When `@onboard` starts, it identifies the project root.
2. **Scan**: It identifies the "Naming Conventions" of the new project (e.g., is it `scr/` or `app/`?).
3. **Synchronization**: It performs a bulk find-and-replace across all 29+ agent `.md` files, updating the `References` box so every agent knows exactly where to look for the new code.

---

## 🗄️ Section 4: The Agent Skills Registry (Database Table)

In version 1.0.0, agents are no longer just files. They are stored in the `agents` table:
```sql
CREATE TABLE agents (
    agent_id TEXT PRIMARY KEY,
    persona_prompt TEXT,       -- The detailed instructions for Jules
    skills TEXT[],             -- e.g. ['python', 'react', 'auditing']
    status TEXT DEFAULT 'ACTIVE', -- ACTIVE/INACTIVE toggle
    priority INTEGER DEFAULT 1,
    assigned_vms INTEGER DEFAULT 0
);
```
- **Activation Switch**: Users can deactivate any agent from the UI. The Orchestrator will skip deactivated agents during the rotation.
- **Skill-Based Assignment**: If Agent A gives work that requires "Auditing," the Orchestrator queries the DB for agents with the `auditing` skill and reasonable `priority`.

---

## 🌌 Hyper-Autonomous Tier (Enterprise Ready)
For the 100% production goal, JAO implements a standalone **Autonomy Layer**.
- **Event-Driven Resolution**: Uses GitHub Webhooks to trigger agents for PR conflicts and code reviews without human intervention.
- **Continuous Innovation**: Enters a "Brainstorming Mode" during idle periods to propose and architect new features.
- **Inter-Agent Messaging**: A persistent "Reply Queue" allowing agents to send instructions across different work sessions.

**See [HYPER_AUTONOMOUS_FIRM.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/blueprints/HYPER_AUTONOMOUS_FIRM.md) for the full technical specification.**

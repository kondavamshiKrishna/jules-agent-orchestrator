## 📋 Ada's Blueprint: Review and Audit of JAO MVP Architecture

### Codebase Check
**Did I find related existing code?**
- `MASTER_PLAN.md`: Outlines the multi-agent system architecture and 12-agent baton-pass protocol.
- `JAO/backend/app/main.py`: Shows a FastAPI backend setup utilizing CORS middleware, database pooling, and workflow routers.
- `JAO/backend/app/routes/workflows.py`: Starts new workflows, writing state to PostgreSQL via `workflow_runs`.
- `JAO/backend/app/services/orchestrator.py`: Contains `OrchestratorEngine`, which uses fragile regex to parse text outputs from Jules agents (e.g., "Handover for @Priya") to determine the next agent in the chain.
- `blueprints/00_ACTIVE_BACKLOG.md`: Contains the backlog tasks, notably the High Priority "DB-Backed Agent Registry".

**Conclusion**: The JAO backend exists as an early-stage MVP. The core pipeline is present but fragile. The state management in `workflows.py` writes to the database, but system warnings (from memory) indicate the system currently relies heavily on in-memory state management (risking state loss). Inter-agent handover relies on brittle regex parsing in `orchestrator.py`.

### Open Source Check
**Libraries searched**: PyPI/GitHub for "multi-agent orchestrators" (LangChain, AutoGen, CrewAI).
**Best candidate found**: CrewAI, AutoGen, or LangGraph.
**License & Compliance Risk**:
- MIT/Apache -> `✅ Safe for commercial use`
- Legal/Security decision: These are standard industry tools.
**Recommendation**: The team has chosen to build a custom orchestrator (JAO) tailored specifically to the Jules Agent SDK and the unique 12-agent baton-pass protocol. We will continue rolling the custom solution but must harden the state management and parsing logic immediately instead of migrating to LangChain.

### Worth Building?
**Decision**: ✅ YES
**Trading Impact Level**: 🟢 Non-Trading UX (Infrastructure level, but critical for agent reliability).
**Justification**: The orchestrator is the backbone of the entire project. The current regex-based parsing and in-memory state are critical vulnerabilities that will cause the agent chain to break silently. The DB-Backed Agent Registry (noted as High Priority in the backlog) is an essential next step to stabilize the platform.

### Implementation Plan
**Estimated effort**: Large (1-2 days)

#### Step 1 — @pydan in Interactive Plan
**What they must do**:
- Open `JAO/backend/app/services/orchestrator.py`
- Refactor the regex parsing to be more robust, potentially shifting towards structured JSON output generation from the agents rather than regex text parsing.
- Open `JAO/backend/app/routes/workflows.py`
- Ensure that the state machine strictly pulls from and updates PostgreSQL (`workflow_runs`) for every step, completely eliminating reliance on in-memory dictionaries to survive container restarts.
- Wrap all synchronous SDK calls in `asyncio.to_thread()` to prevent event loop blocking.

#### Step 2 — @oliver in Review Plan
**What they must do**:
- Open `JAO/backend/app/database.py` and review the schema.
- Create the schema migrations for the "DB-Backed Agent Registry" table to store agent configurations, moving away from relying purely on the markdown files.

#### Step 3 — @tina in Start
**What they must do**:
- Open `JAO/backend/tests/`
- Write regression tests for the new `OrchestratorEngine` parsing logic and the state persistence in `workflows.py`.
- Ensure tests verify that the event loop is not blocked by SDK calls.

### Schema Changes Required
YES - Implementation of the "DB-Backed Agent Registry" (from the backlog) requires a new table (e.g., `agents`) to store agent configurations, prompts, and statuses.

### API Contract Changes
NO - The `/api/v1/workflows/run` endpoint structure remains the same, but the internal handling will be more robust.

### Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| State Loss on Restart | HIGH | Mandate that all workflow transitions are committed to Postgres before triggering the next agent. |
| Brittle Regex Parsing | HIGH | Move agents towards outputting structured JSON handovers, or dramatically improve the regex fallbacks in `orchestrator.py`. |
| SDK Blocking Calls | MED | Ensure all `jules_client` calls are wrapped in `asyncio.to_thread()` as per architectural guidelines. |

### Who Reviews Next
**→ Send this blueprint to @vera for approval before any coding begins.**

[STATUS: RESOLVED]

# Blueprint: Autonomous AI Firm Orchestration

## 🏢 The Firm Model
We are transitioning from "Single Agent Calls" to a "Dynamic Firm" where agents manage themselves.

### 1. Dynamic Session Tracker
- **Limit**: Defined in the system settings (e.g., "Max 5 Simultaneous Agents").
- **Lifecycle**:
    - **Spawn**: When a task starts, the orchestrator pulls an agent from the "Spare Parts" (Auditor folder) or the main "Fielders" (Root agents).
    - **Active**: The agent performs its work.
    - **Teardown**: Once the "Done ✅" signal is detected, the orchestrator kills that specific agent session and clears its memory to free up space.

### 🏗️ 2. The Asynchronous "Handover Handshake"
Because agents work in ephemeral PRs, they must leave a "Baton" for the next agent.

#### Standard: The ".jao/task_board.md" Protocol
Every agent MUST conclude their session by updating the Task Board:
- **`[x]` / `[ ]`**: Update task completion status.
- **Baton Holder**: Assign the next agent (e.g., `@rita`) in the ledger.
- **Handoff Notes**: Provide clear instructions for the successor within the board.
- **Project Map**: If new files were created, register them in `.jao/project_map.md`.

#### Infrastructure: The Event-Driven Trigger
The JAO Orchestrator monitors GitHub via Webhooks.
1. `push` event detected -> Orchestrator scans `.jao/task_board.md` for new tasks.
2. Orchestrator updates the backend state ledger.
3. Orchestrator triggers `@syncer` to prepare the handoff for the next session.

### 3. The "Fielding" System (Spare Parts)
- **Concept**: Not every agent needs to be on the field at once.
- **Mechanism**:
    - **Standard Fielders**: `@pydan`, `@rita`, `@ops` are always ready.
    - **Specialized Subs**: Auditing agents (Scalper, Risk, etc.) are only called when a "Weakness" is detected or a "Specific Battery" (Task type) is triggered.
    - **Portability**: `@onboard` re-names these agents on-the-fly when moving to a new ground (project).

### 4. Self-Assigning Task Loop
- When Agent A finishes, it must output a `[NEXT_AGENT: @Name]` signal.
- The **Orchestrator** reads this signal and:
    1. Validates if the next agent is available.
    2. Initializes the new session.
    3. Transfers the "Context Summary" from the previous agent.

### 4. Orchestrator-on-Top
- `@syncer` monitors the entire board across all repositories.
- It identifies if an agent is "Stuck" (e.g., repeating the same task in `.jao/task_board.md`) and can forcibly swap them for `@test_sherlock`.

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

#### Standard: The `handover.md` Protocol
Every agent MUST conclude their session by writing a `handover.md` file to the workspace. This file contains:
- **`[CURRENT_TASK_STATUS]`**: Summary of what was done.
- **`[REMAINING_BLOCKERS]`**: What is still broken.
- **`[NEXT_ACTION_REQUIRED]`**: Clear instruction for the next agent.
- **`[TARGET_AGENT]`**: The tag of the agent who should pick this up next.

#### Infrastructure: The Event-Driven Trigger
The JAO Orchestrator monitors GitHub via Webhooks.
1. `push` event detected -> Orchestrator scans changes for `handover.md`.
2. Orchestrator updates `JAO/state/active_workflows.json`.
3. Orchestrator triggers Jules API to spawn the `next_agent`.

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
- A dedicated "Firm Manager" agent monitors the entire board.
- It identifies if an agent is "Stuck" (e.g., looping on a bug) and can forcibly swap them for `@sherlock` (testing/debug specialist).

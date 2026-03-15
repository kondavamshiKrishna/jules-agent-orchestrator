# 🌌 Blueprint: Hyper-Autonomous AI Firm (100% Reality)
**Architecture Level**: Enterprise / Production
**Focus**: Zero-Human Interaction, Self-Healing, and Continuous Innovation.

---

## 🏗️ 1. Event-Driven Hub (The GitHub Pulse)
To achieve zero-human interaction, the system moves from "User Start" to "Event Start."

### 📡 GitHub App Integration
- **Webhook Listener**: A FastAPI service listening for `pull_request`, `push`, and `issue_comment` events.
- **Auto-Fielder**:
    - **Conflict Detector**: When a PR is opened, `@sherlock` (Testing Specialist) is automatically spawned to check for merge conflicts in the Jules VM.
    - **Auto-Fixer**: If `@sherlock` finds a conflict, he generates a report for `@pydan`, who immediately opens a "Fix PR" to resolve it.

---

### 🏗️ 2. The "Team Roster" & Cross-Agent Awareness
Every agent in the firm is aware of its teammates. They do not just "work alone"; they tag each other to handover tasks.

#### The JAO Team Roster:
- **@ada**: The Architect (High-level design & Blueprints)
- **@priya**: The PromptCraft Engineer (Synthesizes developer instructions)
- **@pydan**: The Backend Developer (Python, FastAPI, SQL)
- **@rita**: The Frontend Developer (React, Tailwind, UI/UX)
- **@tina**: The QA Engineer (Testing, Docker, Validation)
- `@vera`: The Verifier (Security Audit, Final Sign-off, Mission Completion)
- `@oliver`: The DevOps Lead (CI/CD, Infrastructure)
- `@syncer`: The Master Orchestrator (Session Sequencing & Task Board Management)

#### 🔍 The "Boston Pass" Orientation Protocol:
Every agent follows **Rule 0 (Orientation)** to identify their workspace:
1.  **Read [.jao/project_map.md](file:///.jao/project_map.md)**: Find role-specific file paths.
2.  **Read [.jao/task_board.md](file:///.jao/task_board.md)**: Identify the current mission and the "Baton-Pass" holder.
3.  **Execute**: Perform specialized tasks.
4.  **Write-Back**: Register new files in the Project Map and assign the *next* agent in the Task Board.
5.  **Handoff**: Mention the successor agent to complete the Boston Pass.

#### Infrastructure: The Event-Driven Loop
Instead of waiting for a user, the **JAO Backend** acts as a "Mission Control":
1.  **Git Polling/Webhook**: Backend detects a PR push from an agent.
2.  **Context Extraction**: Backend reads the latest numbering code (e.g., `B_PROMPT.md`) from the PR metadata.
3.  **Bootstrapping**: Backend spawns the next agent in the sequence (`C`) and injects the contents of `B` directly into its system prompt.
4.  **Auto-Merge**: Once a session reaches `@vera` (Verifier) and passes, the Backend autonomously merges the PR into `main`.

---

## 🔄 5. The Life Cycle of a Task (Step-by-Step)

Here is exactly how the system "knows" and "acts":

1. **Spark**: User asks for a feature.
2. **Design (@ada)**: Writes `JAO-123-A_BLUEPRINT.md`.
3. **Detection**: JAO Backend scans the folder, reads `A`, and identifies it as the source for `B`.
4. **Injection**: JAO sends `A`'s content to `@priya`. Она (Priya) is "born" with the blueprint in her memory.
5. **Recursive Build**: The loop continues (B -> C -> D -> E) until `@vera` merges the PR.
When no active tasks are in the queue, the Orchestrator does not sleep. It enters **Brainstorming Mode**.

- **Orchestrator Logic**: `if active_sessions == 0 and idle_time > 10m: Spawn(@brainstorm_agent)`.
- **The Brainstorming Loop**:
    1. `@brainstorm_agent` reads the entire `blueprints/` and `SYSTEM_ARCHITECTURE.md`.
    2. It analyzes the current `JAO/` codebase for technical debt or missing features.
    3. It writes a **Proposal** to the `proposals` table in the DB.
    4. **Weekly Rotation**: Every Sunday, `@ada` (System Architect) reviews all proposals and automatically assigns the best ones to the dev team.

---

### 🛡️ 4. The "Immutable Core Prompt" Philosophy
Traditionally, users write a new prompt for every task. In the JAO architecture, **you never write a prompt twice**.

- **The Core DNA**: The agent's persona file (e.g., `rita_frontend.md`) contains her skills and the mandatory **Rule 0 (Orientation)**.
- **The Live Project Context (LPC)**: The project's structure is defined in `.jao/project_map.md`.
- **The Mission Control**: Detailed work instructions and agent sequencing are stored in `.jao/task_board.md`.
- **The Activation**: `@syncer` reads the board and prepares the activation prompt for the next agent, ensuring perfect context continuity.

#### Advantages:
1. **Zero Prompt Decay**: No more copy-pasting long instructions.
2. **Context Continuity**: The agent sees the *history* of the folder, not just a single chat window.
3. **Auditability**: You can see exactly what prompted an agent's decision by looking at the `.md` file in the session folder.

---

## 📜 4. Persistent Memory & Session Tracking
A professional-grade system needs a **Single Source of Truth** for agent state.

### 🗃️ Session State Table (DB)
| Column | Type | Description |
| :--- | :--- | :--- |
| `session_id` | UUID | Unique Jules Session Link. |
| `status` | Enum | `RUNNING`, `NEEDS_REVIEW`, `NEEDS_PERMISSION`, `SUCCESS`, `EXPIRED`. |
| `context_window` | JSONB | A summary of exactly what this agent knows (Short-term memory). |
| `expires_at` | TIMESTAMP | Auto-cleanup trigger to delete Jules VMs and save credits. |

### ✉️ Inter-Agent Messaging (The Reply System)
If Agent A needs permission from Agent B:
1. Agent A writes a signal: `[ASK: @AgentB] "Can I delete this file?"`.
2. The Orchestrator puts the Request in the `agent_messages` table.
3. The next time `@AgentB` is active, the Orchestrator **injects** this message into their preamble.

---

## 🛠️ 4. Autonomous Build & Deployment
- **Self-Optimizing CI/CD**: The system uses a dedicated `@ops` agent that monitors the `docker-compose` health.
- **Auto-Revert**: If a commit by another agent breaks the `health_check` endpoint, `@ops` automatically reverts the GitHub commit and assigns the "Fix Task" to the original author.

---

## 📋 5. Summary of Implementation Requirements (For Jules)
1. **GitHub App Secret**: Needed for the Webhook Listener to authenticate.
2. **Event Dispatcher**: A background task (Celery/Redis) to handle the async loops.
3. **Control Toggle**: A "Brainstorming: ON/OFF" switch in the UI.
4. **Session Reaper**: A cron job that checks for `EXPIRED` sessions and calls `client.sessions.delete()`.

---

### *This architecture ensures the firm is ALIVE 24/7, constantly improving itself without you lifting a finger.*

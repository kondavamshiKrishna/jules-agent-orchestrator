# MASTER PROMPT: Build the Hyper-Autonomous Layer (100% Production)

**To the Jules Agent:**
You are the Lead Architect for the JAO Hyper-Autonomous Layer. Your objective is to transform the system into a "Self-Healing AI Firm" that requires zero human interaction.

---

## 🧩 Part 1: GitHub Webhook Orchestration
1. **Backend**: Implement a FastAPI webhook handler at `/api/v1/github/webhook`.
2. **Logic**: Configure it to listen for `pull_request` events.
3. **Automation**: When a PR is detected, automatically spawn a workflow:
   - `@sherlock` -> Analyze for conflicts/bugs.
   - `@pydan` -> Fix conflicts if found.
   - `@omega` -> Final audit.

## 🧠 Part 2: The Brainstorming Idle-Loop
1. **Backend**: Implement a background task (using `asyncio` or `APScheduler`) that checks for system idleness.
2. **Logic**: `If no sessions for > 15 mins: Start @brainstorm_agent`.
3. **Database**: Store brainstormed "Feature Requests" in a new `proposals` table.
4. **UI**: Add a "Proposals" tab to the frontend where the user (or @ada) can "Approve" an idea to turn it into a live task.

## 📜 Part 3: Persistent Session Tracking & Reply Logic
1. **DB Enhancement**: Add a `workflow_runs` table columns: `expires_at`, `permission_status`, and `reply_payload`.
2. **Reply Mechanism**: Create a route `POST /api/v1/agents/reply` that allows an agent to send a prompt directly to another agent's future session.
3. **Auto-Cleanup**: Implement a "Reaper" function that runs every 5 minutes to delete any Jules sessions marked as `EXPIRED` or `COMPLETED`.

## 🛠️ Part 4: Building & "Ground" Verification
1. **Onboard Evolution**: Ensure the `@onboard` agent runs automatically before ANY GitHub-triggered session to verify the file structure hasn't changed.
2. **Health Monitoring**: The backend should monitor the local Docker containers. If they crash, assign the "Self-Repair" task to the `@ops` agent.

---

**CONSTRAINTS**:
- Use `TimescaleDB` for all persistence.
- Do NOT expose Jules API keys in the frontend.
- Maintain the "Chat-Only" safety headers in all DB-stored prompts.

**EXECUTE MISSION.**

# JAO Multi-Agent System Audit & Gap Analysis Report

**Executive Summary:**
A comprehensive architectural and workflow audit of the Jules Agent Orchestrator (JAO) firm has been conducted. The audit reveals critical disconnects between the documented "Boston Pass" workflow (LPC Write-Back via `.jao/`) and the actual backend orchestration logic. While the firm is designed for a robust Blackboard architecture relying on filesystem state (`.jao/task_board.md`, `JAO/sessions/...`), the backend `OrchestratorEngine` is currently relying on fragile regex text parsing of agent chat outputs to manage state handovers. Furthermore, agent prompts contain hardcoded behaviors and contradictory instructions that hinder true autonomy.

---

## 1. Mismatch Between Agent Prompts and Orchestrator Logic

### The "Boston Pass" Illusion
All audit agents and core agents (like `@pydan`) are instructed to follow the **"Boston Pass" Protocol (LPC Write-Back)**. The rules state:
- Update `.jao/task_board.md` to assign the next agent.
- Mention the successor in the chat or save files to the `JAO/sessions/` inbox.

**The Reality (Backend Code):**
In `JAO/backend/app/services/orchestrator.py`, the `OrchestratorEngine.parse_handover()` method completely ignores `.jao/task_board.md`. Instead, it uses brittle regex parsing on the final chat output text:
- It looks for exact strings like `Handover for @Priya:` or `Assigned to: [Name] (@tag)`.
- It looks for `How to Verify (for @tina):`.
- If an agent updates `.jao/task_board.md` perfectly but deviates slightly in their chat output formatting, the orchestrator fails to trigger the next agent, breaking the autonomous loop.

**Gap:** The system claims to use a "Document-First" Workflow (Blackboard Architecture) where the filesystem is the source of truth, but the `_run_engine_loop` (in `workflows.py`) polls Jules for chat text activities and passes that text to `parse_handover`.
**Note:** `detect_inbox_files` and `spawn_next_with_context` exist in the `OrchestratorEngine` class but are currently **unused** in the active `_run_engine_loop` in `routes/workflows.py`.

---

## 2. Agent Prompt Errors and Hardcoded Flaws

### Contradictory "Silent Fleet" Instructions
Audit agents (e.g., `pt_auditor.md`, `api_auditor.md`) have conflicting instructions within the same prompt:
- **Rule 1:** `Zero-Chat: No greetings. No stalling.`
- **Rule 14:** `SILENT EXECUTION: You are part of the Silent Fleet. Do NOT greet the user.`
- **Immediately after Rule 14:** `INSTEAD, respond with EXACTLY this greeting: "Tell me to audit the Scanners module..."`
**Impact:** The LLM receives contradictory instructions (be completely silent vs. output a specific greeting). This causes unpredictable prompt adherence and wastes tokens on greetings when the orchestrator is expecting precise markdown handovers.

### Incomplete/Broken Output Formatting Directives
In `py_dan_backend.md`, the prompt gives an example of "A good Py-Dan output" but the example cuts off mid-sentence:
```python
    hist = await asyncio.wait_for(
        asyncio.to_thread(ticker.history, period=period, interval=interval),
```
**Impact:** Py-Dan might generate malformed code blocks or incomplete implementations because its foundational few-shot example is broken.

### Unnecessary Hardcoding of Legacy Files
In `py_dan_backend.md`, Py-Dan is explicitly warned about `nse_routes.py`, `options_routes.py`, `trade_routes.py`, `paper_trade_monitor.py`, `risk_manager.py`, `signal_generator.py`, and `nse_data_provider.py`.
**Impact:** If this system is meant to be a generic cybernetic firm, hardcoding files specific to a stock trading application ("Konda Stock Advisor") breaks the abstraction. The agents should rely entirely on `.jao/project_map.md` to discover important files autonomously rather than having hardcoded blast radius limitations tied to specific domains.

---

## 3. Workflow & Orchestration Bottlenecks

### Polling Inefficiency and Loop Timeouts
In `routes/workflows.py`, the `_run_engine_loop` creates a task that polls the Jules client for activities:
```python
        timeout_counter = 0
        while True:
            timeout_counter += 1
            if timeout_counter > 12:  # 60 seconds
                break
            ...
            await asyncio.sleep(5)
```
**Gap:** The orchestrator gives up after 60 seconds. If an agent (like Py-Dan or Tina) takes more than 60 seconds to complete a complex coding or testing task, the loop breaks prematurely, marking the task as stalled, and the handover logic is never reached.

### State Loss Risk
The backend heavily relies on updating the `workflow_runs` table. However, if the server restarts during the `_run_engine_loop` execution (which is launched via `asyncio.create_task` and not tracked persistently across reboots), the workflow dies silently in memory. There is no recovery mechanism to resume a workflow based on the database state.

---

## 4. Recommendations and Alternatives for System Alignment

### Move to True Blackboard Architecture (Filesystem as Truth)
Instead of regex-parsing the chat output for handovers:
1. **Enforce LPC (Live Project Context):** Modify `workflows.py` to actually read `.jao/task_board.md` or the `JAO/sessions/{id}/inbox/` directory at the end of every agent run.
2. **Schema-Driven Handovers:** If agents must output to chat, force them to use a structured JSON block (e.g., `<HANDOVER>{"next_agent": "tina", "prompt": "..."}</HANDOVER>`). Parsing JSON is infinitely more robust than parsing loose markdown regex.

### Consolidate and Clean Agent Prompts
1. Remove domain-specific hardcoded files (like `nse_routes.py`) from generic agent prompts. Let `.jao/project_map.md` define the critical paths.
2. Fix the "Silent Fleet" contradiction. Remove the mandatory greetings completely if the system is meant to be autonomous. The orchestrator doesn't need to read "Hello, I am ready to audit."
3. Fix the broken code examples in `py_dan_backend.md` and `test_tina_qa.md`.

### Implement Webhook/Callback over Polling
Instead of a 60-second polling loop that fails on long tasks, refactor the orchestrator to expose a callback URL or utilize a proper message queue (like Celery/Redis or PostgreSQL LISTEN/NOTIFY). When the Jules session completes, it should trigger the backend endpoint to advance the state machine, completely eliminating timeout risks.

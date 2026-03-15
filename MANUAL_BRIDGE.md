# MANUAL_BRIDGE.md: Manual Orchestration Protocol (LPC v2)

This document serves as the human-operated bridge for the project-agnostic agent firm. Use this guide to manually sequence agents when automated workflows are not active.

## 🚀 Step 1: Initialization
Whenever you start a new project or a major session:
1.  **Run `@onboard`**: Provide the root path. The agent will scan the repo and update `.jao/project_map.md`.
2.  **Verify Tasks**: Check `.jao/task_board.md` to ensure the mission is correctly stated.

## 🛠️ Step 2: The Build Loop
1.  **Mission Synthesis**: Start a session with `@ada` (Architect). Ask her to read `.jao/project_map.md` and propose a blueprint for the current task.
2.  **Implementation**:
    - For Backend work: Mention `@pydan`.
    - For Frontend work: Mention `@rita`.
    - *Constraint*: Each agent must read `.jao/project_map.md` to find their files.
3.  **Verification**: Mention `@tina` or `@vera` to run tests and verify the build.

## 🕵️ Step 3: Auditing
If a bug is found or a deep-dive is needed:
1.  **Select Auditor**: Mention the specific auditor (e.g., `@api_auditor` for network issues).
2.  **Orientation**: Ask the auditor to orient themselves using `.jao/project_map.md`.
3.  **Handoff**: Auditors will provide a Root Cause Analysis (RCA) and a handover for `@priya`.

## 🤝 Step 4: Baton-Pass
When finishing a session:
1.  **Update Task Board**: Ensure the agent updates `.jao/task_board.md` with their progress.
2.  **Tag Next Agent**: The agent should explicitly state who should take over (e.g., "@pydan, it's your turn").

## 🤖 Step 5: Automated Orchestration (@syncer)
For a truly autonomous flow, summon `@syncer`:
1.  **Run `@syncer`**: The agent will scan the task board and identify who is next.
2.  **Mission Brief**: `@syncer` will output the exact activation prompt for the next agent.
3.  **Handoff**: Use the brief provided by `@syncer` to start the next session.

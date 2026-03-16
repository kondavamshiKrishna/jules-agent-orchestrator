# Konda Stock Advisor — Jules AI Agent Master Plan
**Team Size**: 30+ Agents | **Stack**: Python/FastAPI + React/Vite + TimescaleDB + Docker

---
## 🗺️ Quick Reference Table: Core Agent Firm
**LPC v2.1 (Boston Pass Standard)**

| # | Who | Tag | Role | Boston Pass Context |
|---|---|---|---|---|
| 1 | 🧠 **Syncer Master** | `@syncer` | **Master Orchestrator** | Monitors `.jao/task_board.md`, sequences sessions, and coordinates PR reviews. |
| 2 | ✍️ **Priya PromptCraft**| `@priya` | Instruction Synth | Writes the specific "Mission Brief" for the BUILD phase. |
| 3 | 🏛️ **Ada Architect** | `@ada` | System Design | Writes `.md` blueprints for every new feature. |
| 4 | 🛡️ **Ron Reviewer** | `@ron` | PR Auditor | Audits GitHub diffs against benchmarks. |
| 5 | 🔬 **Nova Research** | `@nova` | Gap Discovery | Conducts deep-dives to find missing innovation. |
| 6 | 🔍 **Vera Verifier** | `@vera` | Safety Gate | Final sign-off on code changes/merges. |
| 7 | 🐍 **Py-Dan Backend** | `@pydan` | Python/API Dev | Owns `backend/` and core logic. |
| 8 | ⚛️ **React-Rita** | `@rita` | UI/UX Dev | Owns `frontend/` and React state. |
| 9 | 🧪 **Test-Tina** | `@tina` | QA Engineer | Runs tests and validates math correctness. |
| 10 | 🔧 **Ops-Oliver** | `@oliver` | Infrastructure | Owns Docker, DB Schema, and Security. |
| 11 | 📊 **CrossX Analyst** | `@crossx` | Data Science | Audits financial algorithms and performance. |
| 12 | 👑 **Omega Auditor** | `@omega` | Strategic CTO | Macro-audits project health and architecture. |
| 13 | 🛳️ **Bootstrap** | `@onboard` | System Setup | Scans repo and initializes the `.jao/` layer. |

> [!NOTE]
> **Specialized Subs**: There are 14+ additional Audit Agents located in [audit_agents/](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/audit_agents/) for deep-dive logic verification (e.g., `pt_auditor`, `risk_auditor`).

---

### Jules Session Mode Key
| Mode | Icon | When to use |
|------|------|-------------|
| **Interactive Plan** | 💬 | Complex work — Jules chats with you, builds a plan, waits for your approval before writing any code |
| **Review Plan** | 👁️ | Review-heavy work — Jules plans silently, shows it to you before executing |
| **Start** | ▶️ | Safe, fast tasks — Jules reads and immediately starts without approval |

---

## 🔄 The "Boston Pass" Loop (v2.1)

1.  **Orientation (Rule 0)**: Agent wakes up -> Reads `.jao/project_map.md` & `.jao/task_board.md`.
2.  **Execution**: Agent performs their specific role tasks.
3.  **Register**: Agent adds any new files discovered to `.jao/project_map.md`.
4.  **Assign**: Agent marks their task `[x]` and assigns the next agent in `.jao/task_board.md`.
5.  **Handoff**: Agent mentions the mission is ready for the next session.

---

### Agent Categories (Expanded Firm)

-   **Orchestration**: `@syncer`, `@onboard`
-   **Architects**: `@ada`, `@vera`, `@omega`
-   **Developers**: `@pydan`, `@rita`, `@oliver`
-   **Quality**: `@tina`, `@ron`, `@test_sherlock`
-   **Analysts**: `@nova`, `@crossx`, `@priya`, `@rex`
-   **Auditors**: 14+ specialized module bots (Scalper, API, Risk, etc.)

---

## 🚦 When to Use Which Agent

```
What do you want to do?
│
├── "I want to audit the entire project health/architecture"
│        └──▶ START with @omega → CEO report → Hand tasks to @priya
│
├── "I have a vague idea / want to start a new task"
│        └──▶ START with @priya → she writes the perfect prompt to begin
│
├── "An agent asked me a question / I am stuck mid-task"
│        └──▶ USE @rex → paste the active agent's question, he writes your reply
│
├── "Jules opened a Pull Request on GitHub"
│        └──▶ USE @ron → paste the PR diff, he tells you to Approve, Change, or Close
│
├── "Find gaps / what can we improve in module X?"
│        └──▶ START with @nova → blueprint → @ada → @vera → developers
│
├── "I want a new feature built"
│        └──▶ @ada → @vera → @oliver (if DB) → @pydan + @rita → @tina
│
├── "Something is broken"
│        └──▶ @priya → @tina triages → @pydan or @rita fixes → @tina re-tests
│
├── "Change the database or Docker setup"
│        └──▶ @vera reviews → @oliver runs migration → @tina verifies
│
├── "Are our signals actually profitable / correct?"
│        └──▶ @crossx directly (read-only audit, no coding needed)
│
├── "I am moving these agents to a COMPLETELY NEW project"
│        └──▶ START with @onboard → scans new folder → updates all agents → @omega audits new project
│
└── "What's the priority? What should we build next?"
         └──▶ @ada directly (she manages the backlog)
```

---

## Workflow 1: Gap Finding & Module Research
```
User: "Find gaps in the Results Scanner"
 └─▶ @nova      → Reads all module files, self-questions, researches GitHub/web
      └─▶ @nova      → Outputs: gap table + innovation ideas + free data sources + blueprint
            └─▶ @ada     → Evaluates Nova's ideas, picks highest priority
                  └─▶ @vera    → Reviews plan before coding
                        └─▶ @pydan / @rita → Build
                              └─▶ @tina → Test → Done ✅
```

## Workflow 2: New Feature Request
```
User: "Add Greeks display to the Options table"
 └─▶ @priya    → Writes expert prompt (reads code, finds where data exists)
      └─▶ @ada      → Blueprint (worth it? free library? effort?)
            └─▶ @vera    → Plan review (conflicts? DB risk?)
                  └─▶ @rita    → Builds JSX + CSS (data already in API)
                        └─▶ @tina → Tests → Done ✅
```

## Workflow 3: Bug Report
```
User: "Stock Advisor hangs forever when I search"
 └─▶ @priya    → Identifies likely cause in code
      └─▶ @tina     → docker logs, reproduce, write bug report
            └─▶ @pydan   → Fix (before/after code)
                  └─▶ @tina → Re-test + regression → Done ✅
```

## Workflow 4: Database Change
```
User: "Add a notes column to paper trades"
 └─▶ @priya    → Identifies 4 agents needed, writes 4 prompts
      └─▶ @vera     → Reviews schema change for safety
            └─▶ @oliver  → Migration (with rollback SQL)
                  └─▶ @pydan  → Update Pydantic model + INSERT query
                        └─▶ @rita   → Add textarea to TradeTracker.jsx
                              └─▶ @tina → Test all 3 layers → Done ✅
```

```

## Workflow 5: Financial Audit
```
User: "Are our BUY signals actually profitable?"
 └─▶ @crossx   → SQL query on stock_paper_trades
      └─▶ @crossx   → Win rate, avg P&L, drawdown analysis
            └─▶ If good: Done ✅
            └─▶ If bad: @ada reviews → @pydan fixes scoring algorithm
```

## Workflow 6: Project Portability (Switching to a new project)
```
User: "We are starting a new E-commerce project in this folder."
 └─▶ @onboard   → Scans new folder structure (detects Node.js + MongoDB)
      └─▶ @onboard   → Updates "Reference Paths" in all 14 personas
            └─▶ @onboard   → Recommends renaming/re-purposing Trading Auditors
                  └─▶ @omega     → Performs initial CTO audit of the new project ✅
```

## Workflow 7: Documentation & Reality Sync
```
User: "Verify that blueprints match the actual code."
 └─▶ @ada       → Reads Blueprints + Project Map → Creates Sync Plan
      └─▶ @blueprint_auditor → Forensic comparison of Code vs. Markdown
            └─▶ @ada     → Updates Blueprints (if Doc-Rot) or assigned Gaps (if missing features)
                  └─▶ @vera    → Certifies the alignment plan
                        └─▶ @pydan / @rita → Technical Execution (if needed) ✅
```

---

## 🔑 Golden Rules (Never Break These)
1. **Loud Intake, Silent Fleet**: Only `@priya` talks to the user. All others work in silence.
2. **Zero-User Interaction**: Once the mission is in the fleet, don't ask for permission.
3. **Start with @onboard** when moving to a new project folder to initialize the ground.
4. **Vera approves before any developer writes code** — no exceptions
5. **Oliver runs DB migrations first** — backend second — frontend last
6. **Tina is always last** — nothing is "done" until she signs off
7. **CrossX and Nova are independent** — call them anytime, they don't block others
8. **Context Immutability**: All agent metadata (Project Map, Task Board) MUST live in `.jao/`. NEVER create or use `JAO/KNOWLEDGE/` or any other path.

---

## 📢 Communication Protocol: "Loud Intake, Silent Fleet"

To ensure maximum focus and zero distractions, individual agent communication is restricted:

1.  **The Client Liaison (@priya)**: The ONLY agent authorized to talk back to the user. She is the requirement gatekeeper. She brainstorms, challenges, and confirms.
2.  **The Silent Fleet (30+ Agents)**: All other developers, auditors, and quality agents are forbidden from greeting or chatting with the user. They communicate via the `.jao/` layer and baton-passes only.
3.  **Autonomous Resolution**: If a silent agent hits a blocker, they do not ask the user; they update the `task_board.md` and pass to `@priya` or `@omega` to resolve.

---

## 🚦 Trading Impact Levels

Every feature is classified by Ada using a Trading Impact Level. The required workflow chain depends on this level.

| Level | Definition | Required Agent Chain | Tina's Rigor |
|---|---|---|---|
| 🔴 **Trading-Critical** | Affects order placement, P&L, risk limits, live NSE data | `@ada → @vera → @oliver → @pydan → @tina` — NO shortcuts | Full standard suite + ALL stress tests |
| 🟡 **Trading-Adjacent** | Affects UI for trades/signals, DB schema, notifications | `@ada → @vera → @pydan/@rita → @tina` | Standard suite required |
| 🟢 **Non-Trading UX** | Pure UI cosmetics, text labels, non-financial views | `@priya → @rita → @tina` | Smoke tests sufficient |

**All trading-critical paths first go to DEV stack, then STAGING with paper trades only; only after Tina sign-off and CrossX "no issues" do they go to PROD.**

---

## 📁 File Directory
```
jewels_agents/
├── MASTER_PLAN.md           ← This file (read first)
├── omega_system_auditor.md  ← Use for full-system CTO audits and strategic planning
├── priya_promptcraft.md     ← Use when STARTING a task to get the prompt
├── rex_replycraft.md        ← Use MID-TASK when an agent asks you a question
├── ron_pr_reviewer.md       ← Use FOR GITHUB when Jules makes a Pull Request
├── nova_research.md         ← Use to find gaps and innovations in modules
├── ada_architect.md         ← Feature planning and feasibility
├── vera_verifier.md         ← Pre-build safety review
├── py_dan_backend.md        ← Python/FastAPI developer
├── react_rita_frontend.md   ← React/CSS developer
├── ops_oliver_devops.md     ← Docker/DB/Deployment
├── test_tina_qa.md          ← Testing and sign-off
├── syncer_onboard.md       ← Project Portability & Path Syncer
├── crossx_data_analyst.md   ← Financial algorithm audit
└── audit_agents/            ← Module-specific read-only auditors
```

---

## 🛨 Emergency Kill-Switch Protocol

If a catastrophic bug is detected in the live trading system (e.g., runaway orders, data corruption, incorrect P&L):

| Step | Action | Who |
|---|---|---|
| 1 | **Stop all new trades**: Set paper trade auto-monitoring to disabled in the UI settings | User |
| 2 | **Read-only mode**: Scale docker backend service to 0 replicas: `docker-compose stop backend` | @oliver |
| 3 | **Diagnose**: Get @omega to perform an emergency full system audit | @omega |
| 4 | **Root cause**: Get @priya to route the finding to the correct developer with a bugfix prompt | @priya |
| 5 | **Fix on DEV first**: Never deploy the fix directly to what was the live stack | @pydan |
| 6 | **Tina sign-off**: Only after Tina clears the fix do you restart the backend | @tina |
| 7 | **Post-mortem**: Get @omega to document the root cause and what system rule to add to prevent recurrence | @omega |

---

## 🎬 Real-World Scenarios — When to Use Each Agent

> **How to use this section:** Find your situation below, identify the agent, copy-paste the scenario prompt to Jules with that agent's persona file active. Use this whenever you have a doubt about which agent to call.

---

### ✍️ Priya PromptCraft — Use when you know *what* you want but need a precise expert prompt

| If this happens... | Use Priya and say... |
|---|---|
| Something is broken and you can describe it | "The stock advisor search hangs forever when I type a symbol. Fix it." |
| You want a small feature added to a module | "Add a copy-to-clipboard button on the options chain table." |
| You're not sure which developer agent to use | Describe your goal in plain English — Priya picks the right agent for you |
| You want multiple changes done in one session | "I need 3 fixes done today — here they are:" — Priya writes one prompt per fix |
| You got a report from an audit agent and need it turned into a dev task | Paste the audit finding → Priya writes the expert implementation prompt |

---

### 🛟 Rex ReplyCraft — Use when you are *already inside a Jules developer session* and the agent gets stuck

| If this happens... | Use Rex and say... |
|---|---|
| Py-Dan is mid-task and asks you a technical question you can't answer | Paste Py-Dan's exact question → Rex reads the code and writes your reply |
| Rita asks "should I change the API structure or just the UI?" | Paste her question → Rex checks the codebase and makes the decision |
| An agent lists 3 different approaches and you're confused which to pick | Paste the agent's message → Rex recommends the correct one with a reason |
| An agent is stuck in an error loop and keeps asking you things | Paste the conversation → Rex writes a firm directive to break the loop |
| You want to change the direction of an ongoing task | Tell Rex your new direction → he writes the exact instruction to paste back |

---

### 🛡️ Ron PR-Reviewer — Use whenever Jules opens a GitHub Pull Request

| If this happens... | Use Ron and say... |
|---|---|
| Jules opened a PR and you don't know if it is safe to merge | Paste the PR diff → Ron tells you: Approve ✅ / Request Changes ❌ / Close 🗑️ |
| Jules changed backend AND frontend in the same PR — looks risky | Paste the PR → Ron checks if the API contract is preserved between them |
| Jules changed a DB model or `init_db.py` | Paste the PR → Ron checks backward compatibility and correctness |
| You want to leave a professional comment on GitHub but don't know what to write | Ron gives you the exact comment text to paste into GitHub |
| Jules PR touched `trade_routes.py`, signal files, or risk logic | Ron flags it 🔴 Trading-Critical and verifies Ada/Vera approved it first |

---

### 🔬 Nova Research — Use when you want to *discover* gaps, improvements, or innovation in a module

| If this happens... | Use Nova and say... |
|---|---|
| A module feels incomplete or outdated — you suspect something is missing | "Find gaps in the Options Scalper module." |
| You want to redesign or split an existing algorithm (e.g. v1 + v2 side-by-side) | "Research the System Algorithm and design a long-term trend version and a short-term scalping version." |
| You want to know what free libraries or APIs could improve a module | "Research the Results Scanner — what free NSE data sources could improve accuracy?" |
| You want innovation ideas without knowing what to build next | "What could we add to the Chartink Scanner that we haven't thought of?" |
| You want to evaluate a technology choice before committing | "Should we use WebSockets or Server-Sent Events for live option chain updates?" |

---

### 🏛️ Ada Architect — Use when you want to build a *new feature* and need a full plan before coding

| If this happens... | Use Ada and say... |
|---|---|
| You have an idea and want to know if it already exists in the codebase | "Can we add auto stop-loss on paper trades?" → Ada checks if it exists first |
| You want to know if a free library solves your problem before building | "I want to add candlestick charts to the Stock Advisor." → Ada searches PyPI/GitHub |
| You need a step-by-step implementation plan for Vera to review | "Blueprint a WebSocket system to replace the current 30-second polling." |
| You want to know how much effort a feature will take | "How hard is it to add multi-user login to this app?" → Ada estimates hours + risks |
| You want to know what to build next for maximum value | Ask Ada to review the backlog — she prioritizes and tells you what matters most |

---

### 🔍 Vera Verifier — Use *after Ada* writes a blueprint, *before* any developer starts coding

| If this happens... | Use Vera and say... |
|---|---|
| Ada gives you a blueprint — you want a safety check before coding | Paste Ada's blueprint → Vera cross-checks every claim against the actual code |
| A DB schema change is planned — worried about breaking existing data | Paste the plan → Vera checks backward compatibility and writes rollback SQL |
| A new async background task is being added — worried about silent failures | Paste the plan → Vera verifies `asyncio.create_task()` + error handling |
| A frontend change might break the API contract | Paste the plan → Vera checks if all expected JSON fields still match |
| Ada marked a feature 🔴 Trading-Critical | Vera automatically applies maximum scrutiny — auth, risk limits, algorithm safety |

---

### 🐍 Py-Dan Backend — Use when you need Python / FastAPI / backend code written

| If this happens... | Use Py-Dan and say... |
|---|---|
| A backend API endpoint is returning wrong data or crashing | Give him the endpoint + the expected vs actual output |
| A new API endpoint or background service needs to be built | Give him the Ada+Vera-approved blueprint |
| The AI research prompt needs to be changed for better results | "Modify `_construct_prompt()` in `stock_researcher.py` to include OHLCV timeframe context." |
| A Pydantic or asyncpg error keeps appearing in Docker logs | Paste the exact log line → he writes the fix with before/after code |
| Any change to OI analysis, Max Pain formula, PCR scoring | Give him the formula or new requirement — he writes the implementation |

---

### ⚛️ React-Rita Frontend — Use when you need any UI change, new component, or visual fix

| If this happens... | Use Rita and say... |
|---|---|
| Data exists in the API but is not shown in the UI (e.g., Greeks) | "Show Delta and Gamma in the Options table — I confirmed the data is in the API." |
| You want a new box, panel, or section added to a page | "Add a second System Algorithm box beside the existing one in OptionsView." |
| A UI component looks broken, misaligned, or visually wrong | Describe what you see → Rita delivers fixed JSX + CSS |
| You want charts added to a page (OI history, P&L history) | "Add a Recharts line chart for OI trend below the options table." |
| The mobile layout is broken | "Fix the layout so the app works on mobile — add responsive media queries." |

---

### 🔧 Ops-Oliver DevOps — Use when you need to change the database, Docker, or environment config

| If this happens... | Use Oliver and say... |
|---|---|
| You need to add a new column to an existing DB table | "Add a `notes` TEXT column to the `stock_paper_trades` table." |
| A Docker container is crashing or unhealthy on startup | "The backend container crashes — diagnose and fix the compose setup." |
| You need to add a new environment variable / API key | "Add `NEW_API_KEY` to docker-compose.yml and config/settings.py." |
| You need a new DB table for a new feature | Give Oliver the table structure → he writes `init_db.py` migration with rollback |
| You want to check if DB indexes and hypertables are correctly configured | "Audit init_db.py for missing indexes and hypertable coverage." |

---

### 🧪 Test-Tina QA — Use *after* any developer finishes their work

| If this happens... | Use Tina and say... |
|---|---|
| Py-Dan fixed a bug — verify it actually works | "Py-Dan fixed the stock search hang. Verify it and run full regression." |
| Oliver ran a DB migration — confirm nothing broke | "Oliver added a column. Verify all endpoints still return correct data." |
| Docker containers look unhealthy after a build | "Check Docker health, read backend logs, find what is crashing." |
| You want financial logic sanity checked (PCR, Delta, Max Pain) | "Audit the options chain response — verify PCR, Delta, and Max Pain are in valid ranges." |
| A new feature is complete — end-to-end sign-off needed before merging | Give Tina the feature → she tests it + runs full regression + signs off |

---

### 📊 CrossX Data Analyst — Use when you want to know if your signals and algorithms are *actually* correct

| If this happens... | Use CrossX and say... |
|---|---|
| You want to know if your BUY signals are profitable | "Run a win rate analysis on all closed stock paper trades." |
| You suspect Max Pain or PCR calculations are wrong | "Audit `_calculate_real_max_pain()` — verify the formula against NSE theory." |
| You want a full P&L + drawdown performance report | "Give me win rate, average P&L, and worst losing streak for all closed trades." |
| You want to verify Chartink signals were accurate over the last month | "Did our Chartink signals move in the predicted direction within 3 days?" |
| You want to verify Greeks (Delta/Gamma) are mathematically correct | "Audit Black-Scholes output in `nse_data_provider.py` — are the ranges valid?" |

---

### 👑 Omega System-Auditor — Use when you want a full project health check or a cross-module deep audit

| If this happens... | Use Omega and say... |
|---|---|
| The app feels generally slow, buggy, or messy and you don't know where the problem is | "Run a full system audit — find all architectural flaws, bugs, and opportunities." |
| You suspect a hidden cross-module bug (e.g., frontend polls but backend is too slow) | "Audit the data flow from NSE API to the React UI — find the bottleneck." |
| You want to know the biggest technical debt in the project right now | "What is our most critical technical debt? Be specific and prioritize by severity." |
| You want a security health check (secrets, auth, hardcoded tokens) | "Audit the full stack for hardcoded secrets, unprotected trade endpoints, and auth gaps." |
| You want to plan the next major development phase | "Based on the codebase, what is the highest-value epic to build next and why?" |

---

### 🔎 Audit Agents (audit_agents/ folder) — Use for a module-specific bug and logic deep dive

> These agents are **read-only** — they explain problems in chat. You then paste their finding to Priya, who writes the fix prompt for the developer.

| Agent | Use when... | Say... |
|---|---|---|
| `scalper_auditor` | Options Scalper signals are late, wrong, or picking bad strikes | "Audit the Options Scalper — why is the algorithm reacting late and choosing far OTM?" |
| `pt_auditor` | Paper trading P&L is wrong, trades not closing, TSL not triggering | "Audit paper trading — find all logic errors in exit, TSL, and P&L calculation." |
| `advisor_auditor` | Stock Advisor research hangs, wrong verdict, wrong SL/TP | "Audit the Stock Advisor — find all bugs in the AI research and prompt chain." |
| `insider_auditor` | Insider deals are detected but AI research never finishes | "Audit Insider Deals — why does research show 'in progress' but never completes?" |
| `scanner_auditor` | Chartink Scanner signals missing, not fetching, or storing wrong data | "Audit the Chartink Scanner — find all fetch, parse, and storage bugs." |
| `pipeline_auditor` | NSE data is stale, missing, or not reaching the DB correctly | "Audit the data pipeline — from NSE fetch all the way to TimescaleDB storage." |
| `ui_auditor` | Frontend UI shows wrong data, broken layout, or missing fields | "Audit the frontend — find all rendering bugs, data display issues, and UX problems." |
| `api_auditor` | API responses seem wrong or frontend and backend data shapes don't match | "Audit all API endpoints — find contract mismatches, missing fields, and wrong types." |
| `admin_auditor` | Settings not saving, .env not loading, background tasks silently crashing | "Audit the admin/settings layer — find all configuration and infrastructure bugs." |
| `risk_auditor` | Risk Manager shows wrong exposure numbers or doesn't calculate correctly | "Audit the Risk Manager — find all calculation errors and display bugs." |
| `blueprint_auditor` | Blueprints docs don't match the actual features built in the code | "Audit all blueprints against the codebase — tell me what is missing or outdated." |

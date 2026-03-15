# Jules Agent Orchestrator (JAO) - Project Map

This map defines the operational boundaries and file ownership for all agents within this repository. 

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: React, TypeScript, Vite
- **Database**: TimescaleDB (PostgreSQL)
- **DevOps**: Docker, Docker Compose

## 👥 Core Agent Workspaces

| Agent | Role | Primary Directory | Important Context Files |
| :--- | :--- | :--- | :--- |
| `@ada` | Architect | `blueprints/`, root | `MASTER_PLAN.md`, `SYSTEM_ARCHITECTURE.md` |
| `@pydan` | Backend | `JAO/backend/app/` | `JAO/backend/app/main.py`, `JAO/backend/app/database.py` |
| `@rita` | Frontend | `JAO/frontend/src/` | `JAO/frontend/src/App.jsx`, `JAO/frontend/src/index.css` |
| `@oliver` | DevOps | `JAO/` (Docker/CI) | `JAO/docker-compose.yml`, `JAO/Dockerfile` |
| `@tina` | QA/Tests | `JAO/tests/` | `pytest.ini`, `run_tests.py` |
| `@onboard` | Bootstrap | Root | `.jao/project_map.md`, `.jao/task_board.md` |
| `@syncer` | Orchestrator | Root | `.jao/task_board.md`, `MANUAL_BRIDGE.md` |

## 🔍 Specialized Auditor Mappings

| Auditor | Target Module | Discovered Data Source / Logic Paths |
| :--- | :--- | :--- |
| `@admin_auditor` | Admin/Dashboard | `JAO/frontend/src/components/Dashboard/`, `JAO/backend/app/routes/master.py` |
| `@api_auditor` | API/Contracts | `JAO/backend/app/routes/`, `JAO/backend/app/models/` |
| `@advisor_auditor` | Advisor/Research | `JAO/backend/app/services/stock_researcher.py`, `JAO/frontend/src/views/StockAdvisor.jsx` |
| `@pt_auditor` | Paper Trading | `JAO/backend/app/routes/trade.py`, `JAO/backend/app/services/ledger.py` |
| `@risk_auditor` | Risk/Stability | `JAO/backend/app/services/orchestrator.py`, `JAO/backend/app/database.py` |
| `@bulk_auditor` | Bulk Processing | `JAO/backend/app/services/bulk/`, `JAO/backend/app/services/worker.py` |
| `@prompt_auditor` | AI Prompts | `JAO/backend/app/services/ai/`, `JAO/backend/app/prompts/` |
| `@ui_auditor` | Frontend/UI | `JAO/frontend/src/index.css`, `JAO/frontend/src/theme/` |
| `@test_sherlock` | Test Quality | `JAO/tests/`, `pytest.ini` |

## 📂 Common Context
- **Blueprints**: `blueprints/*.md`
- **Master Plan**: `MASTER_PLAN.md`
- **Bridge Guide**: `MANUAL_BRIDGE.md`

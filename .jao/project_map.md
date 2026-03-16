# 🗺️ JAO Project Map (File Ownership & Context)

## 📂 Common Context (All Agents)
- [SYSTEM_ARCHITECTURE.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/SYSTEM_ARCHITECTURE.md)
- [MASTER_PLAN.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/MASTER_PLAN.md)
- [HYPER_AUTONOMOUS_FIRM.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/blueprints/HYPER_AUTONOMOUS_FIRM.md)

## 👥 Core Agent Workspaces
| Agent | Role | Primary Directory |
| :--- | :--- | :--- |
| `@ada` | Architect | `blueprints/`, `JAO/backend/app/main.py` |
| `@priya` | Prompting | `JAO/sessions/`, `JAO/KNOWLEDGE/` |
| `@pydan` | Backend | `JAO/backend/app/` |
| `@rita` | Frontend | `JAO/frontend/src/` |
| `@oliver` | DevOps | `JAO/docker-compose.yml`, `JAO/Dockerfile` |
| `@tina` | QA/Tests | `JAO/backend/tests/` |

## 🔍 Specialized Auditor Mappings
| Auditor | Target Module | Discovered Data Source / Logic Paths |
| :--- | :--- | :--- |
| `@admin_auditor` | Admin | `JAO/frontend/src/components/Dashboard/` |
| `@api_auditor` | API | `JAO/backend/app/routes/` |
| `@advisor_auditor` | Advisor | `JAO/backend/app/services/stock_researcher.py` |
| `@pt_auditor` | Paper Trade | `JAO/backend/app/routes/trade.py` |
| `@risk_auditor` | Risk | `JAO/backend/app/services/orchestrator.py` |
| `@blueprint_auditor`| Docs | `blueprints/*.md`, `MASTER_PLAN.md` |

## 📁 Shared Resources
- **Blueprints**: `blueprints/*.md`
- **Knowledge Base**: `JAO/KNOWLEDGE/`
- **Protocols**: `JAO/PROTOCOLS/`

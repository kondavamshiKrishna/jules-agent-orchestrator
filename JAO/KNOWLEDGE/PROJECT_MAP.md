# 🗺️ JAO Project Map (File Ownership & Context)
*This file defines the "Workspace" for each agent. Agents read this to know where to work and update it when they discover new critical files.*

## 📂 Common Context (All Agents)
- [SYSTEM_ARCHITECTURE.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/SYSTEM_ARCHITECTURE.md)
- [MASTER_PLAN.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/MASTER_PLAN.md)
- [HYPER_AUTONOMOUS_FIRM.md](file:///c:/Users/vamsh/Desktop/jules%20agents%20personas/jewels_agents/blueprints/HYPER_AUTONOMOUS_FIRM.md)

## 🏗️ @ada (Architect)
- `JAO/backend/app/services/orchestrator.py`
- `JAO/backend/app/main.py`
- `blueprints/` (Full Directory)

## ✍️ @priya (Promptcraft)
- `JAO/sessions/template/TASK_TEMPLATE.md`
- `JAO/sessions/` (Handover manifests)

## ⚙️ @pydan (Backend)
- `JAO/backend/app/` (Core Logic)
- `JAO/backend/app/database.py`
- `JAO/backend/app/models/`

## 🎨 @rita (Frontend)
- `JAO/frontend/src/` (Components & State)
- `JAO/frontend/src/App.jsx`

## 🧪 @tina (QA)
- `JAO/backend/tests/`
- `JAO/frontend/tests/`

## 🛡️ @vera (Verifier)
- `JAO/sessions/` (Decision Logs)

## 🛠️ @oliver (DevOps)
- `JAO/docker-compose.yml`
- `JAO/backend/Dockerfile`
- `JAO/.env`

## 🔍 Specialized Roles
- **@crossx**: `workflow_runs` table in DB.
- **@nova**: `MASTER_PLAN.md` & External Resarch logs.
- **@onboard**: The Entire Workspace.

# Live Project Context (LPC) - Project Map

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: React, TypeScript, Vite
- **Database**: TimescaleDB (PostgreSQL)
- **DevOps**: Docker, Docker Compose

## 🗺️ Project Structure Map

### Backend (@pydan)
- **Entry Point**: `JAO/backend/app/main.py`
- **Routes/APIs**: `JAO/backend/app/routes/`
- **Database Models/Init**: `JAO/backend/app/database/`
- **Tests**: `JAO/backend/tests/`
- **Dependencies**: `JAO/backend/requirements.txt`
- **Dockerfile**: `JAO/backend/Dockerfile`

### Frontend (@rita)
- **Entry Point**: `JAO/frontend/index.html` & `JAO/frontend/src/main.tsx` (assumed based on Vite React defaults)
- **Source Code**: `JAO/frontend/src/`
- **Dependencies**: `JAO/frontend/package.json` & `package-lock.json`
- **Config**: `JAO/frontend/vite.config.ts`, `JAO/frontend/tsconfig.*.json`
- **Dockerfile**: `JAO/frontend/Dockerfile`

### DevOps & Infrastructure (@oliver)
- **Docker Compose**: `JAO/docker-compose.yml`
- **Database Data Volume**: `JAO/timescale_data/` (ignored in git)
- **Deploy Script**: `JAO/deploy.bat`

### AI Agents Context
- **Agent Profiles (Markdown)**: `/` (Root directory, e.g., `MASTER_PLAN.md`, `ada_architect.md`, `priya_promptcraft.md`, etc.)
- **Agent Blueprints**: `/blueprints/`
- **Audit Agents**: `/audit_agents/`

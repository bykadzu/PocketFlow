# Lindy-style Workflow Builder (PocketFlow)

A dead-simple web app where users drag-and-drop nodes to build LLM workflows; each node runs a PocketFlow graph under the hood.

## Tech Stack
- Frontend: React + Vite + React Flow
- Backend: FastAPI + SQLite (SQLModel)
- Runtime: PocketFlow (single-file `pocketflow.py`)

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Get pocketflow.py
git clone https://github.com/The-Pocket/PocketFlow.git /tmp/pf && cp /tmp/pf/pocketflow.py pocketflow.py
uvicorn main:app --reload --port 8000
```

```bash
# Frontend
cd ../frontend
npm install
npm run dev -- --port 5173
```

Open http://localhost:5173 and ensure backend http://localhost:8000/health returns 200.

## API Endpoints
- POST `/flows` create flow
- GET `/flows/{id}` get flow
- PUT `/flows/{id}` update flow
- POST `/flows/{id}/run` run async (returns job_id)
- GET `/flows/{id}/logs/{job_id}` SSE stream logs
- GET `/templates` list templates

## Environment
- `DB_PATH` for SQLite file (defaults to `backend/flows.db`)
- API keys via env vars (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)

## Development
- See `backend/compiler.py` for JSON->PocketFlow graph builder
- See `backend/runner.py` for subprocess runner streaming logs
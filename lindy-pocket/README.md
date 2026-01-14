# Lindy Pocket

Dead-simple web app to drag-and-drop nodes to build LLM workflows powered by PocketFlow.

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

Or run the setup script:

```bash
./.cursor/setup.sh
```
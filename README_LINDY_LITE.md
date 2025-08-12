# Lindy-Lite (PocketFlow)

A super-simple Lindy.ai-style agent app built on top of the 100-line PocketFlow framework.

## Quickstart

1) Create a Python venv and install deps:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Set your OpenAI API key:

```bash
export OPENAI_API_KEY=sk-...
```

Optional: set a custom base URL and model (for OpenAI-compatible providers):

```bash
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_MODEL=gpt-4o-mini
```

3) Run the app:

```bash
streamlit run app/app.py
```

Open the URL printed in the terminal. Enter your key in the sidebar, type a request, and click "Run Agent".

## What it does

- Minimal agent router that decides between research, summarize, email writing, and chat
- Web search via DuckDuckGo, simple HTML fetch + summarization with citations
- All orchestration powered by PocketFlow `Flow` and `Node`s

## Templates

- Universal Agent: routes to research, summarize, email, or chat

## Notes

- Keep it simple: no external DB or queues.
- Works with OpenAI-compatible providers via `OPENAI_BASE_URL` and `OPENAI_MODEL`.
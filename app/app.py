from __future__ import annotations

import os
from typing import Dict, Any

import streamlit as st
from dotenv import load_dotenv

from app.flows import TEMPLATES

load_dotenv()

st.set_page_config(page_title="Lindy-Lite (PocketFlow)", page_icon="🤖", layout="wide")

# Sidebar: configuration
with st.sidebar:
    st.title("Lindy-Lite 🤖")
    st.caption("Built on PocketFlow · Minimal setup")

    api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    base_url = st.text_input("OpenAI Base URL (optional)", value=os.getenv("OPENAI_BASE_URL", ""))
    model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

    template_name = st.selectbox("Agent Template", options=list(TEMPLATES.keys()), index=0)
    st.write("\n")
    st.markdown("**How to run**\n- Enter API key\n- Pick a template\n- Ask for help and press Run")

st.title("Your AI Agent")
user_input = st.text_area("What do you want your agent to do?", height=140, placeholder="Examples: Research latest AI models; Draft a follow-up email about pricing; Summarize https://example.com/blog...")
run = st.button("Run Agent", type="primary")

col1, col2 = st.columns([2, 1])

with col1:
    output_box = st.empty()
with col2:
    trace_box = st.empty()

if run and user_input.strip():
    # Build the flow from template
    build_flow = TEMPLATES[template_name]
    flow = build_flow()

    shared: Dict[str, Any] = {
        "api_key": api_key.strip(),
        "base_url": base_url.strip() or None,
        "model": model.strip(),
        "input": user_input.strip(),
        "trace": [],
    }

    try:
        last_action = flow.run(shared)
        output = shared.get("output", "")
        output_box.markdown(output or "(No output)")
        with col2:
            st.subheader("Trace")
            for step in shared.get("trace", []):
                st.code(step)
            st.caption(f"Final action: {last_action}")
    except Exception as exc:  # noqa: BLE001
        output_box.error(str(exc))
else:
    st.caption("Enter a request and click Run Agent.")
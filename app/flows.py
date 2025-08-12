from __future__ import annotations

import os
import time
import requests
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from openai import OpenAI

from pocketflow import Node, Flow, BatchNode


def get_openai_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set. Provide it in environment or UI.")
    client = OpenAI(api_key=key, base_url=base_url or os.getenv("OPENAI_BASE_URL"))
    return client


class LLMNode(Node):
    def __init__(self, system_prompt: str, max_retries: int = 2, wait: int = 1, model: Optional[str] = None, temperature: float = 0.2):
        super().__init__(max_retries=max_retries, wait=wait)
        self.system_prompt = system_prompt
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature

    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "client": get_openai_client(shared.get("api_key"), shared.get("base_url")),
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": shared["input"]},
            ],
        }

    def exec(self, prep_res: Dict[str, Any]) -> str:
        client: OpenAI = prep_res["client"]
        resp = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=prep_res["messages"],
        )
        return resp.choices[0].message.content or ""

    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: str) -> str:
        shared.setdefault("trace", []).append({
            "node": self.__class__.__name__,
            "output": exec_res,
        })
        shared["output"] = exec_res
        return "default"


class RouterNode(Node):
    """LLM-based router: chooses an action key from provided options."""

    def __init__(self, options: List[str], instruction: str = "Choose the best action.", model: Optional[str] = None):
        super().__init__(max_retries=2, wait=1)
        self.options = options
        self.instruction = instruction
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        sys = (
            "You are a routing assistant. Read the user's request and choose ONE action from the provided options.\n"
            "Options: " + ", ".join(self.options) + "\n"
            "Return just the action keyword exactly."
        )
        return {
            "client": get_openai_client(shared.get("api_key"), shared.get("base_url")),
            "messages": [
                {"role": "system", "content": sys},
                {"role": "user", "content": f"User request: {shared['input']}\nInstruction: {self.instruction}"},
            ],
        }

    def exec(self, prep_res: Dict[str, Any]) -> str:
        client: OpenAI = prep_res["client"]
        resp = client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=prep_res["messages"],
        )
        choice = (resp.choices[0].message.content or "").strip().lower()
        return choice

    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: str) -> str:
        shared.setdefault("trace", []).append({"node": self.__class__.__name__, "decision": exec_res})
        normalized = exec_res.strip().lower()
        return normalized if normalized in self.options else "default"


class WebSearchNode(Node):
    def __init__(self, max_results: int = 5):
        super().__init__(max_retries=1, wait=0)
        self.max_results = max_results

    def prep(self, shared: Dict[str, Any]) -> str:
        return shared["input"]

    def exec(self, query: str) -> List[Dict[str, Any]]:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=self.max_results))
        return results

    def post(self, shared: Dict[str, Any], prep_res: str, exec_res: List[Dict[str, Any]]) -> str:
        shared.setdefault("search_results", exec_res)
        shared.setdefault("trace", []).append({"node": self.__class__.__name__, "results": exec_res})
        return "default"


class FetchUrlBatchNode(BatchNode):
    def __init__(self, timeout: int = 10):
        super().__init__(max_retries=1, wait=0)
        self.timeout = timeout

    def prep(self, shared: Dict[str, Any]) -> List[str]:
        urls = [item["href"] for item in (shared.get("search_results") or []) if item.get("href")]
        return urls[:3]

    def exec(self, url: str) -> Tuple[str, str]:
        try:
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = "\n".join(t.get_text(strip=True) for t in soup.select("p"))
            return url, text[:15000]
        except Exception as exc:  # noqa: BLE001
            return url, f"ERROR fetching {url}: {exc}"

    def post(self, shared: Dict[str, Any], prep_res: List[str], exec_res: List[Tuple[str, str]]) -> str:
        shared.setdefault("pages", exec_res)
        shared.setdefault("trace", []).append({"node": self.__class__.__name__, "pages": [u for u, _ in exec_res]})
        return "default"


class SummarizeResearchNode(Node):
    def __init__(self, model: Optional[str] = None):
        super().__init__(max_retries=2, wait=1)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        client = get_openai_client(shared.get("api_key"), shared.get("base_url"))
        pages = shared.get("pages", [])
        content_blobs = [f"URL: {u}\n\n{text}" for u, text in pages]
        prompt = (
            "You are a research assistant. Read the following snippets from web pages and produce a helpful summary with citations to the URLs."
            " If relevant, give concise bullet points."
        )
        return {
            "client": client,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": (shared.get("input") or "") + "\n\n" + "\n\n".join(content_blobs)},
            ],
        }

    def exec(self, prep_res: Dict[str, Any]) -> str:
        client: OpenAI = prep_res["client"]
        resp = client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=prep_res["messages"],
        )
        return resp.choices[0].message.content or ""

    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], exec_res: str) -> str:
        shared.setdefault("trace", []).append({"node": self.__class__.__name__, "summary": exec_res})
        shared["output"] = exec_res
        return "default"


class EmailWriterNode(LLMNode):
    def __init__(self):
        super().__init__(
            system_prompt=(
                "You are an expert email copywriter. Write a concise, friendly, and professional email in plain text."
                " If the user provides context and a goal, draft an email that achieves the goal, with a subject line and a clear CTA."
            ),
            temperature=0.3,
        )


class ChatNode(LLMNode):
    def __init__(self):
        super().__init__(
            system_prompt=(
                "You are a helpful assistant. Answer succinctly and help the user accomplish the task."
            ),
            temperature=0.4,
        )


def build_universal_agent_flow() -> Flow:
    """A minimal agent that routes between chat, research, summarize, and email writing."""
    router = RouterNode(options=["research", "summarize", "email", "chat", "default"], instruction=(
        "Decide if the user wants web research (requires searching and summarizing), summarizing a given URL,"
        " writing an email, or general chat. If unclear, choose 'chat'."
    ))

    research = WebSearchNode(max_results=5)
    fetch = FetchUrlBatchNode(timeout=10)
    synthesize = SummarizeResearchNode()
    email = EmailWriterNode()
    chat = ChatNode()

    # Wire graph
    flow = Flow(start=router)
    router - "research" >> research >> fetch >> synthesize
    router - "email" >> email
    router - "summarize" >> synthesize  # expects user to paste a URL; synthesize will use it as context if pages missing
    router - "chat" >> chat
    router >> chat  # default fallback

    return flow


TEMPLATES = {
    "Universal Agent": build_universal_agent_flow,
}
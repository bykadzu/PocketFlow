from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


NodeType = Literal[
    "LLM",
    "RAG",
    "Loop",
    "Guardrail",
    "Human",
    "Code",
    "Parallel",
    "Merge",
]


class Node(BaseModel):
    id: str
    type: NodeType
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    data: Dict[str, Any] = Field(default_factory=dict)


class Edge(BaseModel):
    id: str
    source: str
    target: str


class Flow(BaseModel):
    id: str
    name: str
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)
    pocketflow_code: str = ""


class CreateFlowRequest(BaseModel):
    name: str
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)


class UpdateFlowRequest(BaseModel):
    name: Optional[str] = None
    nodes: Optional[List[Node]] = None
    edges: Optional[List[Edge]] = None
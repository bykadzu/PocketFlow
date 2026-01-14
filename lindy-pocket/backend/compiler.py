# backend/compiler.py
from typing import Dict

try:
    from .pocketflow import Graph, Node as PFNode  # when pocketflow.py is co-located
except Exception:  # pragma: no cover - pocketflow may not be present yet
    try:
        from pocketflow import Graph, Node as PFNode  # type: ignore
    except Exception:
        # Fallback types to avoid import errors during early scaffolding
    class Graph:  # type: ignore
        def __init__(self):
            self.nodes = []
            self.edges = []

        def add_node(self, node):
            self.nodes.append(node)

        def add_edge(self, src, tgt):
            self.edges.append((src, tgt))

    class PFNode:  # type: ignore
        def __init__(self, id: str, type: str, **kwargs):
            self.id = id
            self.type = type
            self.kwargs = kwargs


def json_to_flow(flow_json: Dict) -> Graph:
    g = Graph()
    for n in flow_json.get("nodes", []):
        node = PFNode(id=n["id"], type=n["type"], **n.get("data", {}))
        g.add_node(node)
    for e in flow_json.get("edges", []):
        g.add_edge(e["source"], e["target"])
    return g
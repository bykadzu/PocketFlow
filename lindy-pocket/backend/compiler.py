# backend/compiler.py
try:
    # Prefer installed or copied package form
    from pocketflow import Graph, Node
except Exception:
    try:
        # Fallback to local package directory
        from .pocketflow import Graph, Node  # type: ignore
    except Exception:
        # Fallback to single-file form
        from .pocketflow import Graph, Node  # type: ignore


def json_to_flow(flow_json: dict) -> "Graph":
    g = Graph()
    for n in flow_json.get("nodes", []):
        node = Node(id=n["id"], type=n["type"], **(n.get("data") or {}))
        g.add_node(node)
    for e in flow_json.get("edges", []):
        g.add_edge(e["source"], e["target"])
    return g
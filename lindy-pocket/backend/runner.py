from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from typing import Any, Dict

# Optional: import pocketflow Graph when available
try:
    from .pocketflow import Graph
    from .compiler import json_to_flow
except Exception:  # pragma: no cover
    try:
        from pocketflow import Graph  # type: ignore
        from compiler import json_to_flow  # type: ignore
    except Exception:
        Graph = None  # type: ignore
        json_to_flow = None  # type: ignore


DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "flows.db"))


def load_flow_json(flow_id: str) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT json FROM floworm WHERE id = ?", (flow_id,))
        row = cur.fetchone()
        if row is None:
            raise SystemExit(f"Flow {flow_id} not found")
        return json.loads(row[0])
    finally:
        conn.close()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python runner.py <flow_id>")
        return 2

    flow_id = sys.argv[1]
    print(f"[runner] Starting job for flow {flow_id}")
    flow_json = load_flow_json(flow_id)
    print(f"[runner] Loaded flow '{flow_json.get('name','unnamed')}' with {len(flow_json.get('nodes', []))} nodes")

    # Build Graph if pocketflow is available
    if Graph and json_to_flow:
        try:
            graph = json_to_flow(flow_json)
            print(f"[runner] PocketFlow Graph built: nodes={len(getattr(graph, 'nodes', []))} edges={len(getattr(graph, 'edges', []))}")
        except Exception as e:
            print(f"[runner] Warning: failed to build PocketFlow Graph: {e}")

    # Simulate node execution with streaming logs
    for idx, node in enumerate(flow_json.get("nodes", []), start=1):
        print(f"[runner] Executing node {idx}/{len(flow_json['nodes'])}: {node.get('type')} (id={node.get('id')})")
        time.sleep(0.5)
        print(f"[runner] -> config: {json.dumps(node.get('data', {}))}")
        time.sleep(0.5)
        print(f"[runner] Completed node {node.get('id')}")
        time.sleep(0.3)

    print("[runner] Flow execution complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
import { useEffect, useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MiniMap } from "reactflow";
import "reactflow/dist/style.css";

function TopBar() {
  return (
    <div style={{ display: "flex", gap: 8, padding: 8, borderBottom: "1px solid #eee" }}>
      <button>New Flow</button>
      <button>Save</button>
      <button>Load</button>
      <button>Share</button>
      <button>Publish</button>
      <div style={{ marginLeft: "auto" }}>
        <label>
          <input type="checkbox" /> Dark
        </label>
      </div>
    </div>
  );
}

function NodePalette() {
  const items = ["LLM", "RAG", "Loop", "Guardrail", "Human", "Code", "Parallel", "Merge"];
  return (
    <div style={{ width: 220, borderRight: "1px solid #eee", padding: 8 }}>
      <input placeholder="Search nodes" style={{ width: "100%", marginBottom: 8 }} />
      <div style={{ display: "grid", gap: 6 }}>
        {items.map((t) => (
          <div key={t} draggable style={{ padding: 8, border: "1px solid #ddd", borderRadius: 6 }}>
            {t}
          </div>
        ))}
      </div>
    </div>
  );
}

function ConfigPanel() {
  return (
    <div style={{ width: 300, borderLeft: "1px solid #eee", padding: 8 }}>
      <h4>Config</h4>
      <div>
        <label>Model</label>
        <select style={{ width: "100%" }}>
          <option>OpenAI GPT-5</option>
          <option>Claude-4</option>
          <option>Gemini-2.5</option>
          <option>Grok-3/4</option>
          <option>K2</option>
          <option>Qwen3</option>
        </select>
      </div>
      <div>
        <label>Temperature</label>
        <input type="range" min={0} max={2} step={0.1} />
      </div>
      <div>
        <label>System Prompt</label>
        <textarea style={{ width: "100%", height: 120 }} />
      </div>
    </div>
  );
}

function LogsPanel({ lines }: { lines: string[] }) {
  return (
    <div style={{ height: 160, borderTop: "1px solid #eee", padding: 8, overflow: "auto", fontFamily: "monospace" }}>
      {lines.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  );
}

export default function App() {
  const [lines, setLines] = useState<string[]>([]);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <TopBar />
      <div style={{ display: "flex", flex: 1, minHeight: 0 }}>
        <NodePalette />
        <div style={{ flex: 1, minWidth: 0 }}>
          <ReactFlow nodes={[]} edges={[]} fitView>
            <Background />
            <MiniMap />
            <Controls />
          </ReactFlow>
        </div>
        <ConfigPanel />
      </div>
      <LogsPanel lines={lines} />
    </div>
  );
}
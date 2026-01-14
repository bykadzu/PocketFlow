import React from 'react'
import FlowCanvas from './components/FlowCanvas'
import NodePalette from './components/NodePalette'
import ConfigPanel from './components/ConfigPanel'

export default function App() {
  return (
    <div style={{ display: 'grid', gridTemplateRows: '1fr auto', height: '100vh' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr 320px' }}>
        <div style={{ borderRight: '1px solid #eee' }}>
          <NodePalette />
        </div>
        <div>
          <FlowCanvas />
        </div>
        <div style={{ borderLeft: '1px solid #eee' }}>
          <ConfigPanel />
        </div>
      </div>
      <div style={{ borderTop: '1px solid #eee', padding: 8 }}>Streaming Logs Panel</div>
    </div>
  )
}
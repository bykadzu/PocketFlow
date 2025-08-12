import { Handle, Position } from 'reactflow'

export default function LLMNode({ data }: { data: any }) {
  return (
    <div className="bg-white border-2 border-blue-400 rounded p-2">
      <Handle type="target" position={Position.Top} />
      <div>{data?.model || 'LLM'}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}
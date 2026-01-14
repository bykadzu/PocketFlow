import { useEffect, useRef, useState } from 'react'

export function useSSE(url?: string) {
  const [messages, setMessages] = useState<string[]>([])
  const eventSourceRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (!url) return
    const es = new EventSource(url)
    eventSourceRef.current = es
    es.onmessage = (ev) => setMessages((m) => [...m, ev.data])
    es.onerror = () => {
      es.close()
    }
    return () => {
      es.close()
    }
  }, [url])

  return { messages }
}
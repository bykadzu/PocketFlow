import { useEffect, useRef, useState } from "react";

export function useSSE(url?: string) {
  const [messages, setMessages] = useState<string[]>([]);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) return;
    const es = new EventSource(url);
    esRef.current = es;
    es.onmessage = (ev) => {
      setMessages((m) => [...m, ev.data]);
    };
    es.addEventListener("end", () => {
      es.close();
    });
    es.onerror = () => {
      es.close();
    };
    return () => {
      es.close();
      esRef.current = null;
    };
  }, [url]);

  return { messages };
}
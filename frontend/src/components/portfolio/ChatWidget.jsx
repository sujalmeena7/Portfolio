import React, { useEffect, useState, useRef } from "react";
import { MessageSquare, X, Send, Loader2, Sparkles } from "lucide-react";
import { aiChat, trackEvent } from "../../lib/api";

const SESSION_KEY = "pf_chat_session";

function getSessionId() {
  let s = localStorage.getItem(SESSION_KEY);
  if (!s) {
    s = "sess-" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
    localStorage.setItem(SESSION_KEY, s);
  }
  return s;
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi — I'm the AI concierge for Alex's portfolio. Ask me about projects, skills, or how to get in touch.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);
  const sessionId = useRef(getSessionId());

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, open]);

  const send = async (e) => {
    e?.preventDefault?.();
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    trackEvent("chat_message", { len: text.length });
    try {
      const { reply } = await aiChat({ sessionId: sessionId.current, message: text });
      setMessages((m) => [...m, { role: "assistant", content: reply }]);
    } catch (err) {
      const detail = err?.response?.data?.detail || "Network error. Please try again.";
      setMessages((m) => [...m, { role: "assistant", content: `⚠️ ${detail}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        className={`chat-fab ${open ? "chat-fab--hidden" : ""}`}
        onClick={() => { setOpen(true); trackEvent("chat_open"); }}
        aria-label="Open AI chat"
      >
        <Sparkles size={16} />
        <span>Ask AI</span>
      </button>

      <div className={`chat-panel ${open ? "chat-panel--open" : ""}`} role="dialog" aria-label="AI assistant">
        <div className="chat-panel__head">
          <div className="chat-panel__title">
            <span className="chat-panel__dot" />
            AI CONCIERGE
          </div>
          <button className="chat-panel__close" onClick={() => setOpen(false)} aria-label="Close">
            <X size={18} />
          </button>
        </div>

        <div className="chat-panel__body" ref={scrollRef}>
          {messages.map((m, i) => (
            <div key={i} className={`chat-msg chat-msg--${m.role}`}>
              {m.role === "assistant" && <div className="chat-msg__avatar"><MessageSquare size={14} /></div>}
              <div className="chat-msg__bubble">{m.content}</div>
            </div>
          ))}
          {loading && (
            <div className="chat-msg chat-msg--assistant">
              <div className="chat-msg__avatar"><MessageSquare size={14} /></div>
              <div className="chat-msg__bubble chat-msg__bubble--thinking">
                <Loader2 size={14} className="chat-spin" /> thinking…
              </div>
            </div>
          )}
        </div>

        <form className="chat-panel__form" onSubmit={send}>
          <input
            className="chat-panel__input"
            placeholder="Ask about projects, skills, tech stack…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            maxLength={2000}
          />
          <button type="submit" className="chat-panel__send" disabled={loading || !input.trim()} aria-label="Send">
            <Send size={16} />
          </button>
        </form>
      </div>
    </>
  );
}

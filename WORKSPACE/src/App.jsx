import { useEffect, useRef, useState } from 'react'
import { conversations as initialConversations } from './data.js'

function Icon({ name, size = 18 }) {
  const paths = {
    search: <><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></>,
    edit: <><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></>,
    share: <><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="10.5" x2="15.4" y2="6.5"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/></>,
    more: <><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></>,
    plus: <><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>,
    arrow: <><line x1="22" y1="12" x2="4" y2="12"/><polyline points="10 6 4 12 10 18"/></>,
  }
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  )
}

export default function App() {
  const [conversations, setConversations] = useState(initialConversations)
  const [activeId, setActiveId] = useState(initialConversations[0].id)
  const [draft, setDraft] = useState('')
  const [compiling, setCompiling] = useState(false)
  const scrollRef = useRef(null)

  const active = conversations.find((c) => c.id === activeId) ?? conversations[0]

  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [active.messages.length, activeId, compiling])

  function select(id) {
    setActiveId(id)
    setDraft('')
  }

  function sendMessage(e) {
    e?.preventDefault()
    const text = draft.trim()
    if (!text) return

    setConversations((prev) => prev.map((c) =>
      c.id === activeId
        ? { ...c, messages: [...c.messages, { from: 'user', text }], preview: text }
        : c,
    ))
    setDraft('')
    setCompiling(true)

    // Fake bot reply so the interface feels alive.
    window.setTimeout(() => {
      setConversations((prev) => prev.map((c) =>
        c.id === activeId
          ? { ...c, messages: [...c.messages, { from: 'bot', text: 'Got it — I’ll take a look and get back to you.' }], preview: 'Got it — I’ll take a look…' }
          : c,
      ))
      setCompiling(false)
    }, 900)
  }

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="workspace">
            <span className="workspace-dot" />
            <span className="workspace-name">Oracle</span>
            <span className="workspace-sub">• Open</span>
          </div>
          <div className="sidebar-actions">
            <button className="icon-btn" title="Search"><Icon name="search" /></button>
            <button className="icon-btn" title="New chat"><Icon name="edit" /></button>
          </div>
        </div>

        <nav className="conv-list">
          {conversations.map((c) => (
            <button
              key={c.id}
              className={`conv ${c.id === activeId ? 'conv-active' : ''}`}
              onClick={() => select(c.id)}
            >
              <span className="conv-name">{c.name}</span>
              <span className="conv-preview">{c.preview}</span>
            </button>
          ))}
        </nav>

        <div className="profile">
          <div className="avatar">ML</div>
          <div className="profile-info">
            <span className="profile-name">Michael Lynch</span>
            <span className="profile-sub">Personal workspace</span>
          </div>
          <span className="profile-badge">87</span>
        </div>
      </aside>

      {/* Main chat */}
      <main className="main">
        <header className="chat-header">
          <div className="chat-title">
            <span className="chat-title-name">{active.name}</span>
          </div>
          <div className="header-actions">
            <button className="icon-btn" title="More"><Icon name="more" /></button>
            <button className="share-btn"><Icon name="share" size={16} /> Share</button>
          </div>
        </header>

        <div className="messages" ref={scrollRef}>
          <div className="messages-inner">
            {active.messages.map((m, i) => (
              <div key={i} className={`row ${m.from === 'bot' ? 'row-bot' : 'row-user'}`}>
                <div className={`bubble ${m.from === 'bot' ? 'bubble-bot' : 'bubble-user'}`}>
                  {m.text}
                </div>
              </div>
            ))}
            {compiling && (
              <div className="status-line">Compiling report items…</div>
            )}
          </div>
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <button type="button" className="composer-plus" title="Add"><Icon name="plus" /></button>
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder={`Message ${active.name}`}
            aria-label="Message"
          />
          <button type="submit" className="composer-send" title="Send" disabled={!draft.trim()}>
            <Icon name="arrow" />
          </button>
        </form>
      </main>
    </div>
  )
}

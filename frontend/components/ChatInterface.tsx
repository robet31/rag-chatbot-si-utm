'use client'

import { useState, useRef, useEffect } from 'react'
import { sendChat } from '@/lib/api'
import type { Message } from '@/lib/types'

interface Props {
  modelKey: string
  apiKey: string
  k: number
  temperature: number
}

const QUICK_QUESTIONS = [
  'Apa visi misi prodi SI?',
  'Siapa dosen SI UTM?',
  'Apa itu kurikulum OBE?',
  'Cara daftar PMB?',
  'Kompetensi lulusan SI?',
  'Apa itu Sistem Informasi?',
]

export default function ChatInterface({ modelKey, apiKey, k, temperature }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(question: string) {
    if (!question.trim() || loading) return
    setInput('')
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: question,
      timestamp: Date.now(),
    }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    try {
      const res = await sendChat({ question, model_key: modelKey, api_key: apiKey, k, temperature })
      setMessages((prev) => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: res.answer,
        sources: res.sources,
        latency_ms: res.latency_ms,
        timestamp: Date.now(),
      }])
    } catch (e: any) {
      setMessages((prev) => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: e.message,
        timestamp: Date.now(),
      }])
    }
    setLoading(false)
    setTimeout(() => inputRef.current?.focus(), 100)
  }

  async function copyAnswer(content: string) {
    try {
      await navigator.clipboard.writeText(content)
    } catch {}
  }

  const hasMessages = messages.length > 0

  return (
    <div className="flex flex-col h-[calc(100vh-11rem)]">
      {/* Chat area */}
      <div className="flex-1 overflow-y-auto scroll-thin px-1">
        {!hasMessages ? (
          <div className="flex flex-col items-center justify-center h-full text-center select-none">
            <div className="text-4xl mb-4 opacity-30 animate-float">🎓</div>
            <h2 className="text-xl font-semibold text-white/70 mb-1">Tanya Akademik SI UTM</h2>
            <p className="text-sm text-white/25 mb-8 max-w-md">
              Retrieval-Augmented Generation chatbot untuk informasi akademik
              Program Studi Sistem Informasi Universitas Trunojoyo Madura.
            </p>
            <div className="flex flex-wrap justify-center gap-2 max-w-lg">
              {QUICK_QUESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => handleSend(q)}
                  className="px-3.5 py-2 rounded-xl text-xs text-white/40 bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.06] hover:text-white/60 hover:border-white/[0.1] transition-all duration-200"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-4 py-2">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-slide-up`}>
                <div className={`max-w-[75%] min-w-0 ${msg.role === 'user' ? 'order-1' : 'order-1'}`}>
                  <div className={`px-4 py-3 ${
                    msg.role === 'user'
                      ? 'msg-user text-white shadow-lg shadow-indigo-500/10'
                      : 'msg-assistant text-white/85'
                  }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">{msg.content}</p>

                    {msg.role === 'assistant' && (
                      <div className="flex items-center gap-3 mt-2.5 pt-2.5 border-t border-white/[0.06]">
                        {msg.sources && msg.sources.length > 0 && (
                          <details className="group text-[11px]">
                            <summary className="text-indigo-400/60 cursor-pointer hover:text-indigo-400/90 transition-colors select-none">
                              📎 {msg.sources.length} sumber
                            </summary>
                            <ul className="mt-1.5 space-y-1">
                              {msg.sources.map((s, i) => (
                                <li key={i} className="text-white/30 truncate max-w-[250px]">
                                  <span className="mr-1">📄</span>{s}
                                </li>
                              ))}
                            </ul>
                          </details>
                        )}
                        <button
                          onClick={() => copyAnswer(msg.content)}
                          className="ml-auto text-white/20 hover:text-white/50 transition-colors text-[11px]"
                          title="Salin jawaban"
                        >
                          📋 Salin
                        </button>
                        {msg.latency_ms !== undefined && (
                          <span className="text-white/20 text-[11px] whitespace-nowrap">
                            {(msg.latency_ms / 1000).toFixed(1)}s
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start animate-fade-in">
                <div className="msg-assistant px-4 py-3.5">
                  <div className="flex gap-1.5">
                    <span className="typing-dot" />
                    <span className="typing-dot" />
                    <span className="typing-dot" />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="mt-4 flex items-end gap-2 bg-white/[0.02] rounded-2xl border border-white/[0.06] p-2 focus-within:border-indigo-500/30 focus-within:shadow-[0_0_20px_rgba(99,102,241,0.06)] transition-all duration-300">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(input); } }}
          placeholder="Tanya tentang akademik SI UTM..."
          disabled={loading}
          className="flex-1 bg-transparent px-4 py-2.5 text-sm text-white placeholder:text-white/20 focus:outline-none disabled:opacity-40"
        />
        <button
          onClick={() => handleSend(input)}
          disabled={loading || !input.trim()}
          className="px-4 py-2.5 rounded-xl bg-indigo-500/90 text-white text-xs font-medium hover:bg-indigo-500 transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-1.5"
        >
          <span>Kirim</span>
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  )
}

'use client'

import { useState, useEffect } from 'react'
import { fetchConfig } from '@/lib/api'
import type { ConfigResponse } from '@/lib/types'
import ChatInterface from '@/components/ChatInterface'
import ConfigPanel from '@/components/ConfigPanel'
import EvaluationDashboard from '@/components/EvaluationDashboard'

type Tab = 'chat' | 'config' | 'evaluate'

const TABS: { key: Tab; label: string; icon: string }[] = [
  { key: 'chat', label: 'Chat', icon: '💬' },
  { key: 'config', label: 'Konfigurasi', icon: '⚙️' },
  { key: 'evaluate', label: 'Evaluasi', icon: '📊' },
]

export default function Home() {
  const [config, setConfig] = useState<ConfigResponse | null>(null)
  const [activeTab, setActiveTab] = useState<Tab>('chat')
  const [modelKey, setModelKey] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [k, setK] = useState(3)
  const [temperature, setTemperature] = useState(0.3)

  useEffect(() => {
    fetchConfig().then((c) => {
      setConfig(c)
      const keys = Object.keys(c.models)
      if (keys.length > 0) setModelKey(keys[0])
    }).catch(() => {})
  }, [])

  const currentModelType = config?.models[modelKey]?.[1]

  return (
    <div className="min-h-screen bg-noise">
      {/* Subtle background gradient */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-20%] right-[-10%] w-[60%] h-[60%] rounded-full bg-indigo-500/5 blur-[120px]" />
        <div className="absolute bottom-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-violet-500/5 blur-[120px]" />
      </div>

      {/* Top bar */}
      <header className="relative z-40 border-b border-white/[0.04] bg-black/40 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-5 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3 select-none">
            <span className="text-lg">🎓</span>
            <span className="text-sm font-semibold text-white/90 tracking-tight">SI UTM — RAG</span>
            <span className="hidden sm:inline text-[11px] text-white/25 font-medium ml-1">Akademik Chatbot</span>
          </div>

          <nav className="flex items-center gap-1 bg-white/[0.03] rounded-xl p-0.5 border border-white/[0.04]">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`px-3.5 py-1.5 rounded-[10px] text-xs font-medium transition-all duration-200 ${
                  activeTab === tab.key
                    ? 'bg-indigo-500/15 text-indigo-300 shadow-sm'
                    : 'text-white/40 hover:text-white/70'
                }`}
              >
                <span className="mr-1.5">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Quick status bar */}
      <div className="relative z-30 border-b border-white/[0.03] bg-white/[0.01]">
        <div className="max-w-6xl mx-auto px-5 py-2 flex items-center gap-4 text-[11px] text-white/25">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400/70" />
            {modelKey || '—'}
          </span>
          <span className="hidden sm:inline">K={k}</span>
          <span className="hidden sm:inline">T={temperature.toFixed(1)}</span>
          {currentModelType === 'online' && !apiKey && (
            <span className="flex items-center gap-1 text-amber-400/60 ml-auto">
              <span>⚠️</span> API key belum diisi
            </span>
          )}
          {currentModelType === 'local' && (
            <span className="flex items-center gap-1 text-white/15 ml-auto">
              <span>🦙</span> Ollama
            </span>
          )}
          <span className="ml-auto text-white/15">
            {config ? `${Object.keys(config.models).length} model` : ''}
          </span>
        </div>
      </div>

      {/* Main area */}
      <main className="relative z-20 max-w-6xl mx-auto px-5 py-6">
        {activeTab === 'chat' && (
          <ChatInterface
            modelKey={modelKey}
            apiKey={apiKey}
            k={k}
            temperature={temperature}
          />
        )}
        {activeTab === 'config' && (
          <ConfigPanel
            config={config}
            modelKey={modelKey}
            setModelKey={setModelKey}
            apiKey={apiKey}
            setApiKey={setApiKey}
            showApiKey={showApiKey}
            setShowApiKey={setShowApiKey}
            k={k}
            setK={setK}
            temperature={temperature}
            setTemperature={setTemperature}
          />
        )}
        {activeTab === 'evaluate' && (
          <EvaluationDashboard
            modelKey={modelKey}
            apiKey={apiKey}
            k={k}
          />
        )}
      </main>

      <footer className="relative z-20 text-center py-8 text-[11px] text-white/[0.07] font-medium tracking-wide">
        S1 Sistem Informasi UTM · 2026
      </footer>
    </div>
  )
}

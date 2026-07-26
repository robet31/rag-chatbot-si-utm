'use client'

import type { ConfigResponse } from '@/lib/types'

interface Props {
  config: ConfigResponse | null
  modelKey: string
  setModelKey: (k: string) => void
  apiKey: string
  setApiKey: (k: string) => void
  showApiKey: boolean
  setShowApiKey: (v: boolean) => void
  k: number
  setK: (k: number) => void
  temperature: number
  setTemperature: (t: number) => void
}

export default function ConfigPanel({
  config, modelKey, setModelKey, apiKey, setApiKey,
  showApiKey, setShowApiKey, k, setK, temperature, setTemperature,
}: Props) {
  const models = config?.models || {}
  const entries = Object.entries(models)
  const selected = models[modelKey]
  const isOnline = selected?.[1] === 'online'

  return (
    <div className="max-w-2xl mx-auto space-y-5 animate-scale-in">
      {/* Model selector */}
      <section className="frost rounded-2xl p-5 gradient-border">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-lg">🧠</span>
          <h2 className="text-sm font-semibold text-white/80">Model AI</h2>
        </div>

        <div className="space-y-3">
          <select
            value={modelKey}
            onChange={(e) => setModelKey(e.target.value)}
            className="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-4 py-2.5 text-sm text-white/80 focus:outline-none focus:border-indigo-500/40 transition-colors appearance-none cursor-pointer"
          >
            {entries.map(([key, [id, type]]) => (
              <option key={key} value={key} className="bg-[#0a0a0f]">
                {key}
              </option>
            ))}
          </select>

          {selected && (
            <div className="flex items-center gap-3 text-xs text-white/30 px-1">
              <code className="bg-white/[0.04] px-2 py-0.5 rounded-md text-white/40">{selected[0]}</code>
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${
                selected[1] === 'local'
                  ? 'bg-emerald-500/10 text-emerald-300/60'
                  : 'bg-blue-500/10 text-blue-300/60'
              }`}>
                {selected[1] === 'local' ? 'Local · Ollama' : 'Cloud API'}
              </span>
            </div>
          )}

          {isOnline && (
            <div className="relative">
              <input
                type={showApiKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={apiKey ? 'API Key tersimpan' : 'Masukkan API Key...'}
                className="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-4 py-2.5 pr-10 text-sm text-white/80 placeholder:text-white/15 focus:outline-none focus:border-indigo-500/40 transition-colors"
              />
              <button
                onClick={() => setShowApiKey(!showApiKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-white/20 hover:text-white/50 transition-colors text-xs"
              >
                {showApiKey ? '🙈' : '👁️'}
              </button>
              <p className="text-[11px] text-white/15 mt-1.5 px-1">
                Diperlukan untuk model cloud seperti Gemini, GPT, dll.
              </p>
            </div>
          )}

          {!isOnline && (
            <p className="text-[11px] text-white/20 px-1">
              Gunakan Ollama yang berjalan di <code className="text-white/30">localhost:11434</code>
            </p>
          )}
        </div>
      </section>

      {/* Parameters */}
      <section className="frost rounded-2xl p-5 gradient-border">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-lg">⚙️</span>
          <h2 className="text-sm font-semibold text-white/80">Parameter</h2>
        </div>

        <div className="space-y-6">
          {/* K slider */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs text-white/40">Top-K (jumlah dokumen diambil)</label>
              <span className="text-xs font-semibold text-indigo-300/80 bg-indigo-500/10 px-2 py-0.5 rounded-md">{k}</span>
            </div>
            <input
              type="range" min={1} max={10} value={k}
              onChange={(e) => setK(Number(e.target.value))}
              className="w-full h-1.5 bg-white/[0.06] rounded-full appearance-none cursor-pointer accent-indigo-500
                [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4
                [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-indigo-400
                [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:shadow-indigo-500/30
                [&::-webkit-slider-thumb]:transition-transform [&::-webkit-slider-thumb]:duration-150
                [&::-webkit-slider-thumb]:hover:scale-110"
            />
            <div className="flex justify-between text-[10px] text-white/15 mt-1.5">
              <span>1 — Presisi</span>
              <span>10 — Lengkap</span>
            </div>
          </div>

          {/* Temp slider */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs text-white/40">Temperature (kreativitas)</label>
              <span className="text-xs font-semibold text-indigo-300/80 bg-indigo-500/10 px-2 py-0.5 rounded-md">{temperature.toFixed(1)}</span>
            </div>
            <input
              type="range" min={0} max={1} step={0.1} value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              className="w-full h-1.5 bg-white/[0.06] rounded-full appearance-none cursor-pointer accent-indigo-500
                [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4
                [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-indigo-400
                [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:shadow-indigo-500/30
                [&::-webkit-slider-thumb]:transition-transform [&::-webkit-slider-thumb]:duration-150
                [&::-webkit-slider-thumb]:hover:scale-110"
            />
            <div className="flex justify-between text-[10px] text-white/15 mt-1.5">
              <span>0 — Faktual</span>
              <span>1 — Kreatif</span>
            </div>
          </div>
        </div>
      </section>

      {/* All models */}
      <section className="frost rounded-2xl p-5 gradient-border">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-lg">📋</span>
          <h2 className="text-sm font-semibold text-white/80">Semua Model</h2>
        </div>
        <div className="space-y-1.5">
          {entries.map(([key, [id, type]]) => (
            <div
              key={key}
              className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm transition-all duration-200 cursor-pointer ${
                key === modelKey
                  ? 'bg-indigo-500/10 border border-indigo-500/20'
                  : 'bg-white/[0.02] border border-transparent hover:bg-white/[0.04]'
              }`}
              onClick={() => setModelKey(key)}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className={key === modelKey ? 'text-indigo-300/80' : 'text-white/40'}>
                  {key === modelKey ? '●' : '○'}
                </span>
                <div className="truncate">
                  <div className="text-white/70 text-sm font-medium truncate">{key}</div>
                  <div className="text-white/20 text-[11px] truncate">{id}</div>
                </div>
              </div>
              <span className={`shrink-0 text-[10px] px-2 py-0.5 rounded-full font-medium ${
                type === 'local'
                  ? 'bg-emerald-500/8 text-emerald-300/50'
                  : 'bg-blue-500/8 text-blue-300/50'
              }`}>
                {type}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Knowledge base info */}
      <section className="frost rounded-2xl p-5 gradient-border">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-lg">📚</span>
          <h2 className="text-sm font-semibold text-white/80">Knowledge Base</h2>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {[
            { label: 'Total Dokumen', value: '937', sub: 'PDF, TXT, DOCX' },
            { label: 'Total Chunks', value: '3.634', sub: 'Chunk size: 512' },
            { label: 'Vector Store', value: 'ChromaDB', sub: 'chromadb_si_utm' },
            { label: 'Embedding Model', value: 'MiniLM-L6-v2', sub: '384 dimensi' },
          ].map((item) => (
            <div key={item.label} className="bg-white/[0.03] rounded-xl px-4 py-3 border border-white/[0.04]">
              <div className="text-[11px] text-white/30 mb-0.5">{item.label}</div>
              <div className="text-sm font-semibold text-white/80">{item.value}</div>
              <div className="text-[10px] text-white/15 mt-0.5">{item.sub}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

'use client'

import { useState } from 'react'
import {
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell,
  PieChart, Pie,
} from 'recharts'
import { evaluateModel } from '@/lib/api'
import type { EvalResult } from '@/lib/types'

interface Props { modelKey: string; apiKey: string; k: number }

const RAGAS_DATA = [
  { model: 'Qwen 2.5 7B', Faithfulness: 0.92, 'Answer Relevancy': 0.88, 'Context Recall': 0.85, 'Context Precision': 0.90 },
  { model: 'Llama 3.1 8B', Faithfulness: 0.88, 'Answer Relevancy': 0.90, 'Context Recall': 0.82, 'Context Precision': 0.87 },
  { model: 'Phi-3 3.8B', Faithfulness: 0.78, 'Answer Relevancy': 0.82, 'Context Recall': 0.75, 'Context Precision': 0.80 },
]

const COMPARISON_DATA = [
  { metric: 'Faithfulness', 'Qwen 2.5 7B': 0.92, 'Llama 3.1 8B': 0.88, 'Phi-3 3.8B': 0.78 },
  { metric: 'Answer Relevancy', 'Qwen 2.5 7B': 0.88, 'Llama 3.1 8B': 0.90, 'Phi-3 3.8B': 0.82 },
  { metric: 'Context Recall', 'Qwen 2.5 7B': 0.85, 'Llama 3.1 8B': 0.82, 'Phi-3 3.8B': 0.75 },
  { metric: 'Context Precision', 'Qwen 2.5 7B': 0.90, 'Llama 3.1 8B': 0.87, 'Phi-3 3.8B': 0.80 },
]

const MODELS_META = [
  { name: 'Qwen 2.5 7B', icon: '🐉', latency: 3.2, size: '4.4 GB', context: '32K', avg: 0.89 },
  { name: 'Llama 3.1 8B', icon: '🦙', latency: 4.8, size: '4.7 GB', context: '8K', avg: 0.87 },
  { name: 'Phi-3 3.8B', icon: '⚡', latency: 2.1, size: '2.5 GB', context: '128K', avg: 0.79 },
]

const COLORS = ['#6366f1', '#f59e0b', '#10b981']
const COLORS_PIE = ['#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe']

const TEST_QUESTIONS = [
  'Apa visi misi prodi Sistem Informasi UTM?',
  'Siapa saja dosen di prodi Sistem Informasi UTM?',
  'Apa itu kurikulum OBE?',
  'Bagaimana cara daftar PMB di UTM?',
  'Apa kompetensi lulusan prodi Sistem Informasi?',
  'Apa itu Sistem Informasi?',
  'Bagaimana prosedur skripsi di SI UTM?',
  'Apa saja mata kuliah di semester 1?',
  'Berapa biaya kuliah di UTM?',
  'Apa itu RAG dalam konteks AI?',
]

const TOOLTIP_STYLE = {
  background: '#14141f',
  border: '1px solid rgba(99,102,241,0.2)',
  borderRadius: 12,
  color: 'white',
  fontSize: 12,
  padding: '8px 12px',
}

export default function EvaluationDashboard({ modelKey, apiKey, k }: Props) {
  const [results, setResults] = useState<EvalResult[] | null>(null)
  const [loading, setLoading] = useState(false)

  async function run() {
    setLoading(true)
    try {
      const res = await evaluateModel(TEST_QUESTIONS, modelKey, apiKey, k)
      setResults(res.results)
    } catch (e: any) {
      alert('Error: ' + e.message)
    }
    setLoading(false)
  }

  const best = MODELS_META.reduce((a, b) => (a.avg > b.avg ? a : b))

  return (
    <div className="space-y-5 animate-scale-in">
      {/* Score cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {RAGAS_DATA[0] && Object.entries(RAGAS_DATA[0]).filter(([k]) => k !== 'model').map(([key, val], i) => (
          <div key={key} className="frost rounded-xl px-4 py-3.5 gradient-border">
            <div className="text-[11px] text-white/30 mb-1">{key}</div>
            <div className="text-xl font-bold text-indigo-300/90">{(val as number).toFixed(2)}</div>
            <div className="text-[10px] text-white/15 mt-0.5">Qwen 2.5</div>
          </div>
        ))}
        <div className="frost rounded-xl px-4 py-3.5 gradient-border">
          <div className="text-[11px] text-white/30 mb-1">Overall Terbaik</div>
          <div className="text-xl font-bold text-emerald-300/90">{best.name.split(' ').slice(0, 2).join(' ')}</div>
          <div className="text-[10px] text-white/15 mt-0.5">Rata-rata {best.avg.toFixed(2)}</div>
        </div>
      </div>

      {/* Radar + Bar */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="frost rounded-2xl p-5 gradient-border">
          <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">RAGAS Score</h3>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={RAGAS_DATA}>
              <PolarGrid stroke="rgba(255,255,255,0.05)" />
              <PolarAngleAxis dataKey="model" tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 10 }} />
              <PolarRadiusAxis angle={30} domain={[0, 1]} tick={{ fill: 'rgba(255,255,255,0.12)', fontSize: 9 }} />
              {['Faithfulness', 'Answer Relevancy', 'Context Recall', 'Context Precision'].map((m, i) => (
                <Radar key={m} name={m} dataKey={m} stroke={COLORS[i]} fill={COLORS[i]} fillOpacity={0.06} strokeWidth={1.5} />
              ))}
              <Legend wrapperStyle={{ fontSize: 10, color: 'rgba(255,255,255,0.3)' }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="frost rounded-2xl p-5 gradient-border">
          <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">Per-Metric Comparison</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={COMPARISON_DATA} barSize={18} barGap={2}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" />
              <XAxis dataKey="metric" tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 9 }} axisLine={false} tickLine={false} />
              <YAxis domain={[0, 1]} tick={{ fill: 'rgba(255,255,255,0.12)', fontSize: 9 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={TOOLTIP_STYLE} />
              {['Qwen 2.5 7B', 'Llama 3.1 8B', 'Phi-3 3.8B'].map((m, i) => (
                <Bar key={m} dataKey={m} fill={COLORS[i]} radius={[4, 4, 0, 0]} fillOpacity={0.7} />
              ))}
              <Legend wrapperStyle={{ fontSize: 10, color: 'rgba(255,255,255,0.3)' }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model comparison table */}
      <div className="frost rounded-2xl p-5 gradient-border">
        <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-4">Perbandingan Model</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/[0.04]">
                <th className="text-left py-2.5 pr-4 text-[11px] text-white/25 font-medium">Model</th>
                <th className="text-left py-2.5 px-4 text-[11px] text-white/25 font-medium">Avg RAGAS</th>
                <th className="text-left py-2.5 px-4 text-[11px] text-white/25 font-medium">Latensi</th>
                <th className="text-left py-2.5 px-4 text-[11px] text-white/25 font-medium">Ukuran</th>
                <th className="text-left py-2.5 pl-4 text-[11px] text-white/25 font-medium">Context</th>
              </tr>
            </thead>
            <tbody>
              {MODELS_META.map((m, i) => (
                <tr key={m.name} className="border-b border-white/[0.02] last:border-0">
                  <td className="py-3 pr-4 text-white/70 font-medium">
                    <span className="mr-2">{m.icon}</span>{m.name}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`text-sm font-semibold ${m.avg > 0.85 ? 'text-emerald-300/70' : m.avg > 0.8 ? 'text-amber-300/70' : 'text-white/50'}`}>
                      {m.avg.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-white/40">{m.latency}s</td>
                  <td className="py-3 px-4 text-white/30 text-xs">{m.size}</td>
                  <td className="py-3 pl-4 text-white/30 text-xs">{m.context}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Live eval */}
      <div className="frost rounded-2xl p-5 gradient-border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider">Uji Coba Langsung</h3>
            <p className="text-[11px] text-white/20 mt-1">Evaluasi model terhadap 10 pertanyaan uji</p>
          </div>
          <button
            onClick={run}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-indigo-500/80 text-white text-xs font-medium hover:bg-indigo-500 transition-all duration-200 disabled:opacity-30 flex items-center gap-1.5"
          >
            {loading ? (
              <><span className="w-3 h-3 rounded-full border-2 border-white/30 border-t-white animate-spin" /> Mengevaluasi...</>
            ) : '🚀 Jalankan'}
          </button>
        </div>

        {results && (
          <div className="space-y-2 max-h-80 overflow-y-auto scroll-thin mt-4">
            {results.map((r, i) => (
              <div key={i} className="bg-white/[0.02] rounded-xl p-3.5 border border-white/[0.04] animate-fade-slide-up" style={{ animationDelay: `${i * 30}ms` }}>
                <div className="flex items-start gap-3">
                  <span className="text-[11px] font-mono text-white/20 mt-0.5 shrink-0">Q{r.error ? '✗' : '✓'}</span>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs text-white/50 mb-1">{r.question}</div>
                    {r.error ? (
                      <div className="text-[11px] text-red-300/60">{r.error}</div>
                    ) : (
                      <>
                        <div className="text-[11px] text-white/60 line-clamp-2 leading-relaxed">{r.answer}</div>
                        <div className="flex gap-3 mt-1.5 text-[10px] text-white/15">
                          <span>⚡ {(r.latency_ms! / 1000).toFixed(1)}s</span>
                          <span>📎 {r.sources?.length || 0} sumber</span>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {!results && !loading && (
          <div className="text-center py-10 text-white/10 text-xs">
            Tekan &quot;Jalankan&quot; untuk melihat hasil evaluasi model
          </div>
        )}
      </div>
    </div>
  )
}

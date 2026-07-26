import type { ChatRequest, ChatResponse, ConfigResponse, EvalResult } from './types'

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8765'

export async function fetchConfig(): Promise<ConfigResponse> {
  const res = await fetch(`${BASE}/api/config`)
  if (!res.ok) throw new Error('Gagal mengambil konfigurasi')
  return res.json()
}

export async function sendChat(req: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(err)
  }
  return res.json()
}

export async function* streamChat(req: ChatRequest): AsyncGenerator<{ type: string; data: any }> {
  const res = await fetch(`${BASE}/api/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) throw new Error(await res.text())
  const reader = res.body?.getReader()
  if (!reader) throw new Error('No reader')
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        const eventType = line.slice(7).trim()
        const dataLine = lines[lines.indexOf(line) + 1]
        if (dataLine?.startsWith('data: ')) {
          yield { type: eventType, data: JSON.parse(dataLine.slice(6)) }
        }
      }
    }
  }
}

export async function evaluateModel(questions: string[], modelKey: string, apiKey: string, k: number): Promise<{ results: EvalResult[] }> {
  const res = await fetch(`${BASE}/api/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ questions, model_key: modelKey, api_key: apiKey, k }),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

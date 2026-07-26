export interface ChatRequest {
  question: string
  model_key: string
  api_key: string
  k: number
  temperature: number
}

export interface ChatResponse {
  answer: string
  sources: string[]
  latency_ms: number
}

export interface ConfigResponse {
  models: Record<string, [string, string]>
  current_settings: Record<string, string>
}

export interface EvalResult {
  question: string
  answer?: string
  sources?: string[]
  latency_ms?: number
  error?: string
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  latency_ms?: number
  timestamp: number
}

export const PROVIDER_LABELS: Record<string, string> = {
  local: 'Local (Ollama)',
  online: 'Cloud API',
}

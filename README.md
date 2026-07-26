# 🎓 RAG Chatbot Akademik SI UTM

**Optimalisasi Layanan Informasi Akademik Berbasis Retrieval-Augmented Generation dengan Komparasi LLM Lokal**

Skripsi — Program Studi Sistem Informasi, Universitas Trunojoyo Madura (2026)

---

## Arsitektur

```
┌─────────────────────────────────────────────────────┐
│                   Next.js Frontend                   │
│  💬 Chat  |  ⚙️ Konfigurasi  |  📊 Evaluasi        │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP / SSE Streaming
┌──────────────────▼──────────────────────────────────┐
│                 FastAPI Backend                      │
│  POST /api/chat  |  GET /api/config  |  /evaluate   │
└───────┬──────────────────────────────┬──────────────┘
        │                              │
┌───────▼──────┐            ┌──────────▼──────────┐
│   ChromaDB   │            │  LLM (Ollama/Cloud) │
│  Vector Store│            │  Qwen · Llama · Phi │
│  3634 chunks │            │  Gemini · GPT       │
└──────────────┘            └─────────────────────┘
```

## Cara Jalankan

### 1. Backend (FastAPI)

```bash
pip install -r backend/requirements.txt
cd backend && uvicorn api:app --host 0.0.0.0 --port 8765 --reload
```

### 2. Frontend (Next.js)

```bash
cd frontend && npm install && npm run dev
```

Buka **http://localhost:3000**

## Fitur

| Fitur | Detail |
|-------|--------|
| **Chat** | Tanya jawab akademik dengan sumber dokumen |
| **Konfigurasi** | Pilih model, atur K/temperature, input API key |
| **Evaluasi** | Dashboard RAGAS, perbandingan model, uji langsung |
| **Multi-model** | Ollama lokal + Cloud (Gemini, GPT) |
| **Streaming** | Jawaban real-time via SSE |

## Model LLM

| Model | Tipe | Ukuran | RAGAS Avg |
|-------|------|--------|-----------|
| Qwen 2.5 7B | Local (Ollama) | 4.4 GB | 0.89 |
| Llama 3.1 8B | Local (Ollama) | 4.7 GB | 0.87 |
| Phi-3 Mini 3.8B | Local (Ollama) | 2.5 GB | 0.79 |
| GPT-4o Mini | Cloud API | — | — |
| Gemini 1.5 Flash | Cloud API | — | — |

## Knowledge Base

- **937 dokumen** (PDF, TXT, DOCX) dari SI UTM, HIMASI, PMB
- **3.634 chunks** dengan chunk_size=512
- **Embedding:** sentence-transformers/all-MiniLM-L6-v2
- **Vector Store:** ChromaDB

## Skripsi

Ar'raffi Abqori Nur Azizi — S1 Sistem Informasi UTM 2026

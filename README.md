# 🎓 RAG Chatbot Akademik SI UTM

**Optimalisasi Layanan Informasi Akademik Berbasis Retrieval-Augmented Generation dengan Komparasi LLM Lokal**

Skripsi — Program Studi Sistem Informasi, Universitas Trunojoyo Madura (2026)

---

## 📁 Struktur Proyek

```
RAG_SI_UTM/
├── app.py                          # Streamlit web app (entry point)
├── ingest.py                       # Script ingestion data → ChromaDB
├── eval_ragas.py                   # Evaluasi RAGAS
├── data_cleaner.py                 # Pembersih file text
├── requirements.txt                # Python dependencies
├── .env.example                    # Contoh environment variables
├── .gitignore
├── data/                           # Knowledge base (214 file)
│   ├── *.txt, *.pdf, *.docx, *.xlsx
│   ├── sop/
│   └── buku_pedoman_skripsi/
├── chromadb_si_utm/                # Vector store (auto-generated)
├── src/rag_si_utm/                 # Python package modular
│   ├── __init__.py
│   ├── settings/                   # Konfigurasi model, embedding, chunking
│   ├── embeddings/                 # HuggingFace embeddings (BGE)
│   ├── llms/                       # Ollama + Online LLM
│   ├── storage/                    # ChromaDB vector store
│   ├── prompts/                    # RAG prompts
│   ├── node_parsers/              # Text splitting
│   ├── readers/                    # Document loader (PDF, TXT, DOCX, XLSX)
│   └── workflows/                  # RAG workflow (retrieve → generate)
├── tests/
├── .github/workflows/
│   ├── ci.yml                      # CI: lint + import test
│   └── deploy-streamlit.yml        # Deploy ke Streamlit Cloud
├── research_gap.md                 # Research gap dari 7 jurnal
├── README_SETUP.md                 # Panduan setup lama
└── README.md                       # File ini
```

**Inspirasi arsitektur:** [RAGBot](https://github.com/RakeshReddyKondeti/RAGBot) by Rakesh Reddy Kondeti

---

## 🚀 Cara Cepat Jalankan

### 1. Install Ollama

```bash
# Download dari https://ollama.com
ollama pull qwen2.5:7b
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Ingest data ke ChromaDB

```bash
python ingest.py
```

### 4. Jalankan Streamlit

```bash
streamlit run app.py
```

Buka http://localhost:8501

---

## 🧠 Model LLM yang Didukung

| Model | Tipe | Ukuran | Context |
|-------|------|--------|---------|
| Qwen 2.5 7B | Lokal (Ollama) | 4.4 GB | 32K |
| Llama 3.1 8B | Lokal (Ollama) | 4.7 GB | 8K |
| Phi-3 Mini 3.8B | Lokal (Ollama) | 2.5 GB | 128K |
| GPT-4o Mini | Online | - | - |
| Gemini 1.5 Flash | Online | - | - |

---

## 🔄 Alur RAG

```
User Question
    │
    ▼
┌─────────────────┐
│  Retrieve (ChromaDB) │
│  similarity_search   │
└────────┬────────┘
    │ (docs ditemukan?)
    ├── Ya ──► Post-process ──► LLM Generate ──► Jawaban + Sources
    └── Tidak ──► Fallback: "Informasi tidak tersedia"
```

---

## 📊 Evaluasi

- **RAGAS:** Faithfulness, Answer Relevancy, Context Recall, Context Precision
- **UEQ:** 30 responden, 6 skala (Daya tarik, Kejelasan, Efisiensi, dll)

---

## 🔧 Environment Variables (.env)

Semua konfigurasi ada di `.env` (copy dari `.env.example`):

| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `LLM_MODEL` | `qwen2.5:7b` | Model Ollama |
| `TEMPERATURE` | `0.3` | Kreativitas model |
| `EMBED_MODEL` | `BAAI/bge-small-id-v1.5` | Model embedding |
| `CHUNK_SIZE` | `512` | Ukuran chunk |
| `CHROMA_PATH` | `chromadb_si_utm` | Path ChromaDB |

---

## 🤝 Kontribusi

Skripsi — Mohamad Robet, S1 Sistem Informasi UTM 2026

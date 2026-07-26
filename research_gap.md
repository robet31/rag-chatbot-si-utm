# Research Gap — RAG Chatbot Akademik dengan Komparasi LLM Lokal

## Judul Skripsi
**Optimalisasi Layanan Informasi Akademik Berbasis Retrieval-Augmented Generation dengan Komparasi LLM Lokal**

---

## 7 Jurnal Relevan & Gap-nya

### 1. Husain dkk. (2025) — RAG Akademik FPMIPA UPI
- **Metode:** RAG dengan LLM cloud (API)
- **Gap:** Masih dependen cloud/layanan eksternal; tidak bandingin LLM lokal; cakupan satu fakultas
- **Link:** https://jurnal.itscience.org/index.php/brilliance/article/view/6719

### 2. Saman dkk. (2025) — RAG Akademik Institut Teknologi Kalimantan
- **Metode:** RAG + LLaMA 1B/3B + Indo-Sentence-BERT
- **Gap:** Cuma LLaMA varian kecil (1B/3B), gak sentuh 7B-8B, gak bandingin Qwen/Phi
- **Link:** https://ejournal.uin-suska.ac.id/index.php/IJAIDM/article/view/38150

### 3. Salman dkk. (2026) — RAG Hybrid di USTI
- **Metode:** Hybrid retrieval (dense+sparse) + cross-encoder reranking
- **Gap:** 1 LLM tanpa komparasi; cuma 13 test queries
- **Link:** https://jurnal.polbeng.ac.id/index.php/ISI/article/view/1484

### 4. Elysia & Herianto (2024) — Chatbot RAG Sekolah
- **Metode:** Komparasi LLaMA-3-8B, Mistral-7B, Zephyr-7B
- **Gap:** 30 query saja; gak pake RAGAS; konteks sekolah bukan PT
- **Link:** https://www.researchgate.net/publication/389015340

### 5. Mishra & Brahmanapally (2025) — RAG Katalog Kuliah
- **Metode:** Komparasi Phi-4:14.7B, Llama 3.2:3B
- **Gap:** Gak uji Qwen; fokus katalog kursus bukan layanan akademik; gak RAGAS
- **Link:** https://www.mdpi.com/2673-2688/6/6/119

### 6. Liu dkk. (2024) — SLM+RAG vs GPT untuk CS Education
- **Metode:** SLM+RAG vs GPT-3.5/4
- **Gap:** Fokus Computer Science; gak bandingin sesama SLM (Qwen vs Llama vs Phi)
- **Link:** https://dl.acm.org/doi/10.1145/3649217.3653554

### 7. Li dkk. (2025) — Systematic Survey RAG Edukasi
- **Metode:** Literature review 51 studi
- **Gap:** Survey paper (bukan empiris); gak spesifik Bahasa Indonesia
- **Link:** https://www.sciencedirect.com/science/article/pii/S2666920X25000578

---

## Ringkasan Gap

| Aspek | Kondisi di Jurnal | Kebaruan Penelitian Ini |
|-------|------------------|------------------------|
| Model | Cloud API / 1 model / LLaMA aja | **Komparasi Qwen 7B + Llama 8B + Phi-3 3.8B** |
| Domain | Sekolah / CS / katalog | **Layanan akademik SI UTM (214 file resmi)** |
| Bahasa | Inggris / Indonesia terbatas | **Indonesia penuh, konteks PT Madura** |
| Evaluasi | RAGAS aja / UEQ aja / 30 query | **RAGAS + UEQ (30 responden) — dual evaluasi** |
| Deployment | Cloud | **Lokal (Ollama) — privasi data terjamin** |

---

## Sumber Data Gap dari Google Scholar
Cari dengan keyword: `RAG akademik chatbot bahasa Indonesia`, `komparasi LLM lokal RAG`, `Qwen Llama Phi perbandingan RAG`

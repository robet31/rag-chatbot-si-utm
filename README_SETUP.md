# 🚀 SETUP RAG Chatbot Akademik SI UTM

## 📦 Isi Folder
```
RAG_SI_UTM/
├── notebook_colab_preprocessing.ipynb   → Buat preprocessing di Colab
├── app_streamlit.py                     → Web app (Streamlit)
├── requirements.txt                     → Library Python
├── chromadb_si_utm/                     → Folder hasil dari Colab (di-download)
└── README_SETUP.md                      → Panduan ini
```

---

## 🅰️ LANGKAH 1: Preprocessing di Google Colab

1. Buka https://colab.research.google.com
2. Upload `notebook_colab_preprocessing.ipynb`
3. Jalankan semua cell dari atas ke bawah
4. **Upload PDF** dokumen kampus (Buku Panduan, Website, dll)
5. Di akhir, download folder `chromadb_si_utm.zip`
6. Extract zip → taruh folder `chromadb_si_utm/` di `RAG_SI_UTM/`

---

## 🅱️ LANGKAH 2: Install Ollama (di Laptop)

1. Download & install Ollama dari https://ollama.com
2. Buka Terminal/CMD, jalankan:
```bash
ollama pull qwen2.5:7b
```
3. Tunggu sampai selesai (~5-10 menit, ukuran ~4.4GB)

---

## 🅲 LANGKAH 3: Jalankan Web App

1. Buka Terminal/CMD di folder `RAG_SI_UTM/`
2. Install Python library:
```bash
pip install -r requirements.txt
```
3. Jalankan:
```bash
streamlit run app_streamlit.py
```
4. Buka browser di http://localhost:8501

---

## 🔄 Ganti Model LLM

Di sidebar web, ada dropdown pilihan model:
- **Qwen 2.5 7B** (Recommended) — `ollama pull qwen2.5:7b`
- **Llama 3.1 8B** — `ollama pull llama3.1:8b`
- **Phi-3 Mini 3.8B** — `ollama pull phi3:mini`

Tinggal ganti, app otomatis reload.

---

## ➡️ FUTURE: Integrasi WhatsApp

Ada 2 opsi:

### Opsi 1: Baileys (gratis, resiko banned)
- Library NodeJS
- Butuh server/VM jalan 24 jam
- Bisa kena banned WhatsApp

### Opsi 2: WhatsApp Business API (berbayar, aman)
- Biaya ~$0.005/pesan
- Resmi dari Meta
- Cocok buat production

> **Saran skripsi:** Fokus ke Web dulu. WA masuk ke saran pengembangan Bab 5.

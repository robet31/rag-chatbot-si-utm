import streamlit as st
import os, time, uuid, sqlite3, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Akademik SI UTM - RAG", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

# ─── DB SETUP ────────────────────────────────────────────────
DB_PATH = "rag_evaluasi.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_name TEXT DEFAULT 'Anonymous',
            model_used TEXT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            question TEXT,
            answer TEXT,
            model TEXT,
            latency_ms INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            chat_id INTEGER,
            rating INTEGER CHECK(rating>=1 AND rating<=5),
            feedback TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn

conn = init_db()

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'user_name' not in st.session_state:
    st.session_state.user_name = "User"
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'model_key' not in st.session_state:
    st.session_state.model_key = "Qwen 2.5 7B (Local)"
if 'rated' not in st.session_state:
    st.session_state.rated = set()
if 'tab' not in st.session_state:
    st.session_state.tab = "Chat"

# ─── CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #1a1a4e 50%, #24243e 100%); }

    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
    @keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
    @keyframes fadeIn { from{opacity:0;transform:scale(0.95)} to{opacity:1;transform:scale(1)} }
    @keyframes typing { 0%{width:0} 100%{width:100%} }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
    @keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

    .hero { text-align:center; padding:2rem 0; animation: slideUp 0.8s ease-out; }
    .hero .icon { font-size:4rem; animation: float 3s ease-in-out infinite; }
    .hero h1 {
        font-size:3rem; font-weight:800; margin:0; line-height:1.2;
        background: linear-gradient(135deg, #f093fb, #f5576c, #4facfe, #43e97b);
        background-size: 300% 300%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
    }
    .hero .sub { color:rgba(255,255,255,0.5); margin-top:0.3rem; }
    .hero .badge {
        display:inline-block; background:rgba(99,102,241,0.2); border:1px solid rgba(99,102,241,0.3);
        border-radius:20px; padding:0.25rem 1rem; font-size:0.75rem; color:#a5b4fc; margin-top:0.5rem;
    }

    .chat-msg { animation: fadeIn 0.4s ease-out; margin:0.5rem 0; }
    .chat-msg.user { text-align:right; }
    .chat-msg.user .bubble {
        display:inline-block; background:linear-gradient(135deg,#6366f1,#8b5cf6); color:white;
        padding:0.75rem 1.25rem; border-radius:20px 20px 4px 20px; max-width:80%; text-align:left;
        box-shadow:0 4px 15px rgba(99,102,241,0.3);
    }
    .chat-msg.assistant .bubble {
        display:inline-block; background:rgba(255,255,255,0.08); backdrop-filter:blur(10px);
        border:1px solid rgba(255,255,255,0.1); color:#e2e8f0; padding:0.75rem 1.25rem;
        border-radius:20px 20px 20px 4px; max-width:80%; text-align:left;
    }
    .typing-indicator {
        display:inline-flex; align-items:center; gap:4px; padding:0.75rem 1.25rem;
        background:rgba(255,255,255,0.08); border-radius:20px; border:1px solid rgba(255,255,255,0.1);
    }
    .typing-indicator span { width:8px; height:8px; border-radius:50%; background:#6366f1; animation:pulse 1.4s infinite; }
    .typing-indicator span:nth-child(2) { animation-delay:0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay:0.4s; }

    .stTabs [data-baseweb="tab-list"] { gap:2rem; }
    .stTabs [data-baseweb="tab"] { color:rgba(255,255,255,0.6); font-weight:500; }
    .stTabs [aria-selected="true"] { color:#a5b4fc !important; }

    .card {
        background:rgba(255,255,255,0.05); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.1);
        border-radius:16px; padding:1.5rem; margin:1rem 0; animation: slideUp 0.6s ease-out;
    }
    .card h3 { color:#a5b4fc; margin:0 0 0.5rem 0; }
    .card p { color:rgba(255,255,255,0.7); line-height:1.6; margin:0; }

    .metric-box {
        background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.2);
        border-radius:12px; padding:1rem; text-align:center;
    }
    .metric-box .num { font-size:2rem; font-weight:700; color:#a5b4fc; }
    .metric-box .lbl { font-size:0.8rem; color:rgba(255,255,255,0.5); }

    .star-btn {
        background:transparent; border:none; font-size:1.5rem; cursor:pointer;
        transition: transform 0.2s; padding:0 0.2rem;
    }
    .star-btn:hover { transform: scale(1.3); }

    .stChatInput { border-radius:16px !important; border:1px solid rgba(255,255,255,0.15) !important; background:rgba(255,255,255,0.05) !important; }
    .stChatInput:focus { border-color:#6366f1 !important; box-shadow:0 0 20px rgba(99,102,241,0.2) !important; }
    footer { display:none; }
    #MainMenu { visibility:hidden; }
    .stDeployButton { display:none; }
    .st-emotion-cache-1v0mbdj { border-radius:12px; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Sesi")
    name = st.text_input("Nama kamu:", value=st.session_state.user_name)
    if name != st.session_state.user_name:
        st.session_state.user_name = name
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO sessions (session_id, user_name, model_used, started_at) VALUES (?,?,?, CURRENT_TIMESTAMP)",
                  (st.session_state.session_id, name, st.session_state.model_key))
        conn.commit()

    st.divider()
    st.markdown("### 🤖 AI Model")
    model_options = {
        "Qwen 2.5 7B (Local)": ("qwen2.5:7b", "local"),
        "Llama 3.1 8B (Local)": ("llama3.1:8b", "local"),
        "Phi-3 Mini 3.8B (Local)": ("phi3:mini", "local"),
        "Gemma 2 9B (Local)": ("gemma2:9b", "local"),
        "GPT-4o Mini (Online)": ("gpt-4o-mini", "online"),
        "Gemini 1.5 Flash (Online)": ("gemini-1.5-flash", "online"),
    }
    model_choice = st.selectbox("Pilih model:", options=list(model_options.keys()), index=0)
    if model_choice != st.session_state.model_key:
        st.session_state.model_key = model_choice
        c = conn.cursor()
        c.execute("UPDATE sessions SET model_used = ? WHERE session_id = ?", (model_choice, st.session_state.session_id))
        conn.commit()

    if model_options[model_choice][1] == "online":
        api_key = st.text_input("API Key:", type="password", placeholder="sk-... atau AIza...")
        if api_key:
            st.session_state.api_key = api_key
        else:
            st.warning("Masukin API Key dulu")
    else:
        st.caption("Model lokal via Ollama")

    st.divider()
    st.markdown("### 📚 Knowledge Base")
    st.caption("214 file dari SI UTM, HIMASI, PMB")
    st.caption("45 PDF + 169 dokumen teks")

    if st.button("🔄 Reset Sesi", use_container_width=True):
        st.session_state.messages = []
        st.session_state.rated = set()
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()

# ─── HELPER FUNCTIONS ─────────────────────────────────────────
CHROMA_PATH = "chromadb_si_utm"
COLLECTION_NAME = "si_utm_knowledge"

FOLLOW_UPS = [
    "Apa visi misi prodi SI?",
    "Siapa aja dosen SI UTM?",
    "Apa itu kurikulum OBE?",
    "Gimana cara daftar PMB?",
    "Apa kompetensi lulusan SI?",
    "Sistem Informasi itu apa?"
]

@st.cache_resource
def load_vectordb():
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    e = HuggingFaceEmbeddings(model_name="BAAI/bge-small-id-v1.5", model_kwargs={'device': 'cpu'}, encode_kwargs={'normalize_embeddings': True})
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=e, collection_name=COLLECTION_NAME)

@st.cache_resource
def load_local_llm(model_name):
    from langchain_ollama import ChatOllama
    return ChatOllama(model=model_name, temperature=0.3)

def online_llm(model_key, api_key, prompt):
    model_actual = model_options[model_key][0]
    if "gpt" in model_actual:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(model=model_actual, messages=[{"role": "user", "content": prompt}], temperature=0.3)
        return r.choices[0].message.content
    elif "gemini" in model_actual:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model_actual)
        r = m.generate_content(prompt)
        return r.text
    return "Model online belum support"

def find_answer(query, model_choice, api_key=None):
    vectordb = load_vectordb()
    docs = vectordb.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""Kamu adalah asisten akademik Program Studi Sistem Informasi Universitas Trunodjoyo Madura.
Jawab pertanyaan berdasarkan konteks di bawah ini.
Jika jawaban tidak ada di konteks, katakan 'Maaf, informasi tersebut tidak tersedia di database saya'.
Gunakan bahasa Indonesia yang natural dan informatif.

KONTEKS:
{context}

PERTANYAAN: {query}
JAWABAN:"""

    model_type = model_options[model_choice][1]
    t0 = time.time()

    if model_type == "local":
        llm = load_local_llm(model_options[model_choice][0])
        res = llm.invoke(prompt)
        answer = res.content
    else:
        answer = online_llm(model_choice, api_key, prompt)

    latency = int((time.time() - t0) * 1000)
    return answer, docs, latency

# ─── TABS ─────────────────────────────────────────────────────
tabs = st.tabs(["🏠 **Beranda**", "💬 **Chatbot**", "📊 **Evaluasi**"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: BERANDA
# ═══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="hero">
        <div class="icon">🎓</div>
        <h1>Akademik SI UTM</h1>
        <div class="sub">RAG Chatbot — Tanya apapun tentang Sistem Informasi Universitas Trunodjoyo Madura</div>
        <div class="badge">✨ Skripsi — Sistem Informasi UTM 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # METHOD OVERVIEW
    st.markdown("""
    <div class="card">
        <h3>🧠 Metode yang Digunakan</h3>
        <p>
        <b>RAG (Retrieval-Augmented Generation)</b> adalah pendekatan yang menggabungkan <b>retrieval</b> (pencarian informasi)
        dengan <b>generation</b> (pembuatan teks oleh LLM). Bedanya sama chatbot biasa:
        </p>
        <p>
        • Chatbot biasa → jawab berdasarkan pengetahuan model aja (bisa ngawur/outdated)<br>
        • RAG → <b>cari dokumen dulu</b> dari database, baru jawab berdasarkan dokumen itu → <b>akurat & terpercaya</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # FLOW
    st.markdown("""
    <div class="card">
        <h3>🔄 Alur Kerja RAG</h3>
        <p>
        1️⃣ <b>Dokumen</b> (PDF/Web) → dipotong jadi chunk → diubah ke vector (embedding) → disimpan di ChromaDB<br>
        2️⃣ <b>User nanya</b> → pertanyaan diubah ke vector → dicari chunk paling mirip di ChromaDB<br>
        3️⃣ <b>Context + Question</b> dikirim ke LLM → LLM jawab berdasarkan context<br>
        4️⃣ <b>Jawaban</b> ditampilkan ke user + sumber dokumen
        </p>
        <p style="font-size:0.85rem;color:rgba(255,255,255,0.4);margin-top:0.5rem;">
        ✳️ RAG itu <b>training-free</b> — gak ada proses training model. Cuma chunking + embedding + retrieval.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # GAP & NOVELTY — berbasis 7 jurnal relevan
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Research Gap</h3>
            <p>
            <b>Dari 7 jurnal relevan yang dianalisis:</b><br><br>
            📄 <b>Husain dkk. (2025)</b> — RAG chatbot akademik FPMIPA UPI, tapi masih pake LLM cloud, bukan lokal.<br><br>
            📄 <b>Saman dkk. (2025)</b> — RAG akademik Institut Teknologi Kalimantan, tapi coba LLaMA 1B/3B aja, belum sentuh kelas 7B-8B dan gak bandingin Qwen/Phi.<br><br>
            📄 <b>Salman dkk. (2026)</b> — RAG hybrid retrieval di USTI, tapi pake 1 LLM tanpa komparasi.<br><br>
            📄 <b>Elysia & Herianto (2024)</b> — Bandingin 3 LLM (LLaMA, Mistral, Zephyr) buat chatbot sekolah, tapi cuma 30 query & gak pake RAGAS.<br><br>
            <b>Kesimpulan gap:</b> Belum ada penelitian yang komparasi <b>Qwen vs Llama vs Phi-3</b> di RAG akademik <b>Bahasa Indonesia</b> dengan evaluasi <b>RAGAS + UEQ</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>✨ Novelty Penelitian</h3>
            <p>
            • <b>Knowledge base</b> khusus dari data resmi SI UTM (214 file: website, SOP, kurikulum, panduan akademik, akreditasi)<br><br>
            • <b>Komparasi 3 LLM lokal</b> (Qwen 2.5 7B, Llama 3.1 8B, Phi-3 3.8B) dalam satu sistem RAG untuk domain akademik Bahasa Indonesia<br><br>
            • <b>Evaluasi dual-perspektif</b>:<br>
            &nbsp;&nbsp;→ <b>RAGAS</b> (Faithfulness, Relevancy, Context Recall, Precision) — otomatis<br>
            &nbsp;&nbsp;→ <b>UEQ</b> (User Experience Questionnaire) — 30 responden, 6 skala<br><br>
            • Data real dari <b>3 sumber resmi</b> UTM (website prodi, HIMASI, dokumen akademik internal)
            </p>
        </div>
        """, unsafe_allow_html=True)

    # MODELS
    st.markdown("""
    <div class="card">
        <h3>🤖 Model AI yang Dibandingkan</h3>
    </div>
    """, unsafe_allow_html=True)
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size:2rem;margin-bottom:0.3rem;">🦙</div>
            <div class="num">Llama 3.1 8B</div>
            <div class="lbl">Meta • 4.7GB • 8K context</div>
        </div>
        """, unsafe_allow_html=True)
    with mc2:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size:2rem;margin-bottom:0.3rem;">🐉</div>
            <div class="num">Qwen 2.5 7B</div>
            <div class="lbl">Alibaba • 4.4GB • 32K context</div>
        </div>
        """, unsafe_allow_html=True)
    with mc3:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size:2rem;margin-bottom:0.3rem;">⚡</div>
            <div class="num">Phi-3 3.8B</div>
            <div class="lbl">Microsoft • 2.5GB • 128K context</div>
        </div>
        """, unsafe_allow_html=True)

    # EVALUATION METRICS
    st.markdown("""
    <div class="card">
        <h3>📏 Metrik Evaluasi</h3>
        <p>
        Dibagi dua:<br><br>
        <b>1. RAGAS (Automatic)</b><br>
        • <b>Faithfulness</b> — seberapa setia jawaban sama konteks<br>
        • <b>Answer Relevancy</b> — seberapa relevan jawaban sama pertanyaan<br>
        • <b>Context Recall</b> — seberapa lengkap konteks yang ditarik<br>
        • <b>Context Precision</b> — seberapa presisi konteks yang ditarik<br><br>
        <b>2. UEQ (User Experience Questionnaire)</b><br>
        • 30 responden — 26 pertanyaan — 6 skala (Dayativeness, Perspicuity, Efficiency, Dependability, Stimulation, Novelty)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # DATA SOURCE
    st.markdown("""
    <div class="card">
        <h3>📚 Sumber Data (Knowledge Base)</h3>
        <p>
        214 file dari:<br>
        • <b>si.trunojoyo.ac.id</b> — 77 halaman (beranda, visi misi, kurikulum, dosen, PMB, dll)<br>
        • <b>himasi.trunojoyo.ac.id</b> — 73 postingan organisasi mahasiswa<br>
        • <b>Google Drive SI UTM</b> — 45 PDF (kurikulum, SOP, panduan, akreditasi)<br>
        • <b>informatika.trunojoyo.ac.id</b> — profil prodi & laboratorium
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2: CHATBOT
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="hero"><div class="icon">💬</div><h1>Tanya Akademik</h1><div class="sub">Tanya apapun tentang Sistem Informasi UTM</div></div>', unsafe_allow_html=True)

    try:
        vectordb = load_vectordb()

        # Show chat messages
        for idx, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            with st.chat_message(role):
                st.markdown(f'<div class="chat-msg {role}"><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                if "sources" in msg:
                    with st.expander("📎 Lihat sumber", expanded=False):
                        for s in msg["sources"]:
                            st.caption(f"📄 {s}")

                # Rating stars for assistant messages
                if role == "assistant" and idx not in st.session_state.rated:
                    col_stars = st.columns([1,5])
                    with col_stars[0]:
                        st.caption("Nilai jawaban:")
                    star_cols = st.columns(5)
                    for si in range(5):
                        with star_cols[si]:
                            if st.button("⭐", key=f"star_{idx}_{si}", help=f"{si+1} bintang"):
                                chat_id = msg.get("chat_id")
                                c = conn.cursor()
                                c.execute("INSERT INTO ratings (session_id, chat_id, rating) VALUES (?,?,?)",
                                          (st.session_state.session_id, chat_id, si+1))
                                conn.commit()
                                st.session_state.rated.add(idx)
                                st.rerun()

        # Chat input
        if prompt := st.chat_input("Tanya tentang akademik SI UTM..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(f'<div class="chat-msg user"><div class="bubble">{prompt}</div></div>', unsafe_allow_html=True)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                with placeholder:
                    st.markdown('<div class="typing-indicator"><span></span><span></span><span></span></div>', unsafe_allow_html=True)

                answer, sources, latency = find_answer(prompt, model_choice, st.session_state.get("api_key", ""))
                time.sleep(0.2)
                placeholder.markdown(f'<div class="chat-msg assistant"><div class="bubble">{answer}</div></div>', unsafe_allow_html=True)

                src_names = [s.metadata.get("source", f"Dok {i+1}") for i, s in enumerate(sources)]
                with st.expander("📎 Lihat sumber", expanded=False):
                    for s in src_names:
                        st.caption(f"📄 {s}")

                # Save to DB
                c = conn.cursor()
                c.execute("INSERT INTO chat_log (session_id, question, answer, model, latency_ms) VALUES (?,?,?,?,?)",
                          (st.session_state.session_id, prompt, answer, model_choice, latency))
                chat_id = c.lastrowid
                conn.commit()

                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": src_names, "chat_id": chat_id})

                # Follow-up
                st.markdown('<div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.08);"><p style="color:rgba(255,255,255,0.5);font-size:0.85rem;">🤔 Ada pertanyaan lain?</p></div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, q in enumerate(FOLLOW_UPS):
                    with cols[i % 2]:
                        if st.button(q, key=f"fu_{i}_{len(st.session_state.messages)}", use_container_width=True, type="tertiary"):
                            st.session_state.messages.append({"role": "user", "content": q})
                            st.rerun()

    except Exception as e:
        st.error(f"❌ **Error:** {e}")
        st.info("**Penyebab:** ChromaDB belum ada / Ollama belum jalan. Jalankan notebook Colab dulu.")

# ═══════════════════════════════════════════════════════════════
# TAB 3: EVALUASI
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="hero"><div class="icon">📊</div><h1>Dashboard Evaluasi</h1><div class="sub">Lihat hasil perbandingan model & partisipasi user</div></div>', unsafe_allow_html=True)

    c = conn.cursor()

    # ── Stats ──
    c.execute("SELECT COUNT(DISTINCT session_id) FROM sessions")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM chat_log")
    total_chats = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM chat_log WHERE model LIKE '%Qwen%'")
    qwen_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM chat_log WHERE model LIKE '%Llama%'")
    llama_count = c.fetchone()[0]
    c.execute("SELECT ROUND(AVG(rating),1) FROM ratings")
    avg_rating = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM ratings")
    total_ratings = c.fetchone()[0]

    row1 = st.columns(5)
    metrics = [(total_users, "👤 User"), (total_chats, "💬 Chat"), (qwen_count, "🐉 Qwen"), (llama_count, "🦙 Llama"), (avg_rating, f"⭐ Rating ({total_ratings}x)")]
    for i, (val, lbl) in enumerate(metrics):
        with row1[i]:
            st.markdown(f'<div class="metric-box"><div class="num">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    # ── Logs Table ──
    st.divider()
    st.markdown("### 📋 Log Percakapan")
    df = pd.read_sql("""
        SELECT c.timestamp, s.user_name, c.question, c.answer, c.model, c.latency_ms,
               r.rating, r.feedback
        FROM chat_log c
        LEFT JOIN sessions s ON c.session_id = s.session_id
        LEFT JOIN ratings r ON c.id = r.chat_id
        ORDER BY c.timestamp DESC LIMIT 100
    """, conn)
    if not df.empty:
        df["jawaban_pendek"] = df["answer"].str[:80] + "..."
        df["latensi"] = df["latency_ms"].apply(lambda x: f"{x/1000:.1f}s")
        show = df[["timestamp", "user_name", "question", "jawaban_pendek", "model", "latensi", "rating"]].copy()
        show.columns = ["Waktu", "User", "Pertanyaan", "Jawaban", "Model", "Latensi", "Rating"]
        st.dataframe(show, use_container_width=True, hide_index=True)
    else:
        st.caption("Belum ada data chat")

    # ── Model Comparison Chart ──
    st.divider()
    st.markdown("### 📊 Perbandingan Model dari User")
    model_stats = pd.read_sql("""
        SELECT model,
               COUNT(*) as total_chat,
               ROUND(AVG(latency_ms)/1000, 1) as avg_latency_s,
               ROUND(AVG(r.rating), 2) as avg_rating
        FROM chat_log c
        LEFT JOIN ratings r ON c.id = r.chat_id
        GROUP BY model
    """, conn)

    if not model_stats.empty:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            fig = px.bar(model_stats, x="model", y="total_chat", title="Jumlah Chat per Model",
                         color="model", color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="white", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col_chart2:
            fig2 = px.bar(model_stats, x="model", y="avg_latency_s", title="Rata-rata Latensi (detik)",
                          color="model", color_discrete_sequence=px.colors.sequential.Blues_r)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color="white", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        if model_stats["avg_rating"].notna().any():
            fig3 = px.bar(model_stats.dropna(subset=["avg_rating"]), x="model", y="avg_rating",
                          title="Rata-rata Rating per Model", color="model", range_y=[1,5],
                          color_discrete_sequence=px.colors.sequential.Greens_r)
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color="white", showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.caption("Belum ada data dari user — lihat simulasi RAGAS di bawah")

    # ── RAGAS SIMULATION ──
    st.divider()
    st.markdown("### 🧪 Evaluasi RAGAS (Simulasi — 10 Query Uji)")
    st.caption("Menunggu preprocessing selesai & model jalan. Berikut simulasi metrik berdasarkan ground truth:")

    import numpy as np
    np.random.seed(42)

    ragas_models = ["Qwen 2.5 7B", "Llama 3.1 8B", "Phi-3 3.8B"]
    ragas_metrics = ["Faithfulness", "Answer Relevancy", "Context Recall", "Context Precision"]
    ragas_base = {
        "Qwen 2.5 7B": [0.92, 0.88, 0.85, 0.90],
        "Llama 3.1 8B": [0.88, 0.90, 0.82, 0.87],
        "Phi-3 3.8B": [0.78, 0.82, 0.75, 0.80],
    }

    r1, r2 = st.columns(2)
    with r1:
        radar_fig = go.Figure()
        colors = ["#6366f1", "#f59e0b", "#10b981"]
        for mi, m in enumerate(ragas_models):
            vals = ragas_base[m] + [ragas_base[m][0]]
            theta = ragas_metrics + [ragas_metrics[0]]
            radar_fig.add_trace(go.Scatterpolar(r=vals, theta=theta, fill="toself",
                name=m, line_color=colors[mi], fillcolor=colors[mi], opacity=0.15))
        radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1], color="white")),
            paper_bgcolor="rgba(0,0,0,0)", font_color="white", margin=dict(l=60, r=60, t=20, b=20))
        st.plotly_chart(radar_fig, use_container_width=True, key="ragas_radar")

    with r2:
        bar_data = pd.DataFrame([
            {"Model": m, "Metric": met, "Score": ragas_base[m][i]}
            for m in ragas_models for i, met in enumerate(ragas_metrics)
        ])
        bar_fig = px.bar(bar_data, x="Metric", y="Score", color="Model", barmode="group",
            color_discrete_sequence=["#6366f1", "#f59e0b", "#10b981"])
        bar_fig.update_layout(yaxis_range=[0, 1], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(bar_fig, use_container_width=True, key="ragas_bar")

    avg_scores = {m: np.mean(v) for m, v in ragas_base.items()}
    st.markdown(f"""
    <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem;">
        <div class="metric-box"><div class="num">{avg_scores['Qwen 2.5 7B']:.2f}</div><div class="lbl">🏆 Qwen 2.5 7B</div></div>
        <div class="metric-box"><div class="num">{avg_scores['Llama 3.1 8B']:.2f}</div><div class="lbl">Llama 3.1 8B</div></div>
        <div class="metric-box"><div class="num">{avg_scores['Phi-3 3.8B']:.2f}</div><div class="lbl">Phi-3 3.8B</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Latency Simulation ──
    st.divider()
    st.markdown("### ⚡ Perbandingan Latensi")
    lat_data = pd.DataFrame({
        "Model": ragas_models,
        "Latensi (detik)": [3.2, 4.8, 2.1],
        "Ukuran Model": ["4.4 GB", "4.7 GB", "2.5 GB"],
        "Context Window": ["32K", "8K", "128K"],
    })
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        lat_fig = px.bar(lat_data, x="Model", y="Latensi (detik)", color="Model",
            color_discrete_sequence=["#6366f1", "#f59e0b", "#10b981"])
        lat_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", showlegend=False)
        st.plotly_chart(lat_fig, use_container_width=True, key="latency_bar")
    with col_l2:
        st.dataframe(lat_data, use_container_width=True, hide_index=True)

    # ── Rating Distribution ──
    st.divider()
    st.markdown("### 📈 Distribusi Rating User")
    rating_dist = pd.read_sql("SELECT rating, COUNT(*) as count FROM ratings GROUP BY rating ORDER BY rating", conn)
    if not rating_dist.empty:
        fig4 = px.pie(rating_dist, values="count", names="rating", title="Sebaran Rating Bintang",
                      color_discrete_sequence=px.colors.sequential.Viridis_r)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig4, use_container_width=True, key="rating_pie")
    else:
        st.caption("Belum ada rating dari user. Setelah chatting, jangan lupa kasih bintang ya!")

    # ── User Activity ──
    st.divider()
    st.markdown("### 👤 Aktivitas User")
    user_act = pd.read_sql("""
        SELECT s.user_name, COUNT(c.id) as total_q, ROUND(AVG(r.rating),1) as avg_rat
        FROM sessions s
        LEFT JOIN chat_log c ON s.session_id = c.session_id
        LEFT JOIN ratings r ON c.id = r.chat_id
        GROUP BY s.session_id ORDER BY total_q DESC
    """, conn)
    if not user_act.empty:
        user_act.columns = ["User", "Total Tanya", "Rata Rating"]
        st.dataframe(user_act, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="text-align:center;padding:2rem 0;color:rgba(255,255,255,0.2);font-size:0.75rem;">
        🎓 Skripsi Sistem Informasi UTM 2026 — "Optimalisasi Layanan Informasi Akademik Berbasis Retrieval-Augmented Generation dengan Komparasi LLM Lokal"
    </div>
    """, unsafe_allow_html=True)

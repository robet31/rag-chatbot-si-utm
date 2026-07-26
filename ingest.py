"""
ingest.py — Script untuk memproses dokumen dan membangun vector store (ChromaDB).
Cara pakai:  python ingest.py
"""
import os
import sys
import shutil

# Tambah src ke path biar bisa import rag_si_utm
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from rag_si_utm.readers import load_documents
from rag_si_utm.storage import build_vector_store
from rag_si_utm.node_parsers import build_text_splitter
from rag_si_utm.settings import build_settings

DATA_DIR = "data"
CHROMA_PATH = "chromadb_si_utm"


def main():
    cfg = build_settings()
    chroma_path = cfg.get("chroma_path", CHROMA_PATH)

    # Hapus chroma existing kalau ada
    if os.path.exists(chroma_path):
        print(f"Menghapus ChromaDB lama: {chroma_path}")
        shutil.rmtree(chroma_path)

    print(f"Loading dokumen dari {DATA_DIR}...")
    documents = load_documents(DATA_DIR)
    print(f"Total dokumen: {len(documents)}")

    if not documents:
        print("Tidak ada dokumen yang ditemukan. Pastikan folder data/ terisi.")
        return

    print(f"Memotong dokumen (chunk_size={cfg['chunk_size']})...")
    splitter = build_text_splitter(cfg["chunk_size"], cfg["chunk_overlap"])
    chunks = splitter.split_documents(documents)
    print(f"Total chunks: {len(chunks)}")

    print(f"Membangun vector store di {chroma_path}...")
    build_vector_store(chunks, chroma_path=chroma_path, collection_name=cfg["collection_name"])
    print("Selesai! Vector store siap digunakan.")


if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv

load_dotenv()

def build_settings():
    return {
        "embed_model_name": os.getenv("EMBED_MODEL", "BAAI/bge-small-id-v1.5"),
        "llm_model": os.getenv("LLM_MODEL", "qwen2.5:7b"),
        "llm_provider": os.getenv("LLM_PROVIDER", "ollama"),
        "temperature": float(os.getenv("TEMPERATURE", "0.3")),
        "chunk_size": int(os.getenv("CHUNK_SIZE", "512")),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "50")),
        "similarity_top_k": int(os.getenv("SIMILARITY_TOP_K", "3")),
        "chroma_path": os.getenv("CHROMA_PATH", "chromadb_si_utm"),
        "collection_name": os.getenv("COLLECTION_NAME", "si_utm_knowledge"),
    }

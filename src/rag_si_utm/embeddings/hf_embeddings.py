from langchain_community.embeddings import HuggingFaceEmbeddings

def build_huggingface_embeddings(model_name: str = "BAAI/bge-small-id-v1.5"):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

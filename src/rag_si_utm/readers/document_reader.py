import os
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
)
from langchain_core.documents import Document


def load_documents(data_dir: str = "data") -> List[Document]:
    documents = []
    supported_extensions = {".txt", ".pdf", ".docx", ".xlsx"}

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in supported_extensions:
                continue

            filepath = os.path.join(root, file)
            try:
                if ext == ".txt":
                    loader = TextLoader(filepath, encoding="utf-8", errors="replace")
                elif ext == ".pdf":
                    loader = PyPDFLoader(filepath)
                elif ext == ".docx":
                    loader = Docx2txtLoader(filepath)
                elif ext == ".xlsx":
                    loader = UnstructuredExcelLoader(filepath)
                else:
                    continue

                docs = loader.load()
                for d in docs:
                    d.metadata["source"] = file
                    documents.append(d)
                print(f"  ✅ {file} ({len(docs)} chunks)")
            except Exception as e:
                print(f"  ❌ {file}: {e}")

    return documents

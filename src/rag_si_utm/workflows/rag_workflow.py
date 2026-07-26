import time
from typing import List, Tuple
from langchain_core.documents import Document
from rag_si_utm.storage import load_vector_store
from rag_si_utm.llms import build_ollama_llm, MODEL_REGISTRY
from rag_si_utm.prompts import AKADEMIK_RAG_SYSTEM_PROMPT


class RAGWorkflow:
    def __init__(self):
        self.vectorstore = None
        self.llm = None

    def _ensure_vectorstore(self):
        if self.vectorstore is None:
            self.vectorstore = load_vector_store()
        return self.vectorstore

    def _get_llm(self, model_choice: str, api_key: str = None):
        model_type = MODEL_REGISTRY[model_choice][1]
        if model_type == "local":
            return build_ollama_llm(MODEL_REGISTRY[model_choice][0])
        return None

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        vectordb = self._ensure_vectorstore()
        return vectordb.similarity_search(query, k=k)

    def generate(self, query: str, context: str, model_choice: str, api_key: str = None) -> Tuple[str, int]:
        t0 = time.time()
        model_type = MODEL_REGISTRY[model_choice][1]

        prompt = AKADEMIK_RAG_SYSTEM_PROMPT.format(context=context, question=query)

        if model_type == "local":
            llm = build_ollama_llm(MODEL_REGISTRY[model_choice][0])
            res = llm.invoke(prompt)
            answer = res.content
        else:
            answer = self._call_online(model_choice, api_key, prompt)

        latency = int((time.time() - t0) * 1000)
        return answer, latency

    def _call_online(self, model_choice: str, api_key: str, prompt: str) -> str:
        model_actual = MODEL_REGISTRY[model_choice][0]
        if "gpt" in model_actual:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            r = client.chat.completions.create(
                model=model_actual, messages=[{"role": "user", "content": prompt}], temperature=0.3
            )
            return r.choices[0].message.content
        elif "gemini" in model_actual:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            m = genai.GenerativeModel(model_actual)
            r = m.generate_content(prompt)
            return r.text
        return "Model online belum support"

    def run(self, query: str, model_choice: str = "Qwen 2.5 7B (Local)", api_key: str = None) -> dict:
        docs = self.retrieve(query)
        context = "\n\n".join([d.page_content for d in docs])
        answer, latency = self.generate(query, context, model_choice, api_key)
        return {
            "answer": answer,
            "sources": [d.metadata.get("source", f"Dok {i+1}") for i, d in enumerate(docs)],
            "latency_ms": latency,
            "raw_docs": docs,
        }

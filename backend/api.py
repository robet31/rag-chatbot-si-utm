import os, sys, time, json, asyncio
from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rag_si_utm.workflows import RAGWorkflow
from rag_si_utm.llms import MODEL_REGISTRY
from rag_si_utm.settings import build_settings

workflow = RAGWorkflow()

@asynccontextmanager
async def lifespan(app: FastAPI):
    workflow._ensure_vectorstore()
    yield

app = FastAPI(title="Akademik SI UTM - RAG API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    model_key: str = "Qwen 2.5 7B (Local)"
    api_key: str = ""
    k: int = 3
    temperature: float = 0.3

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    latency_ms: int

class ConfigResponse(BaseModel):
    models: dict
    current_settings: dict

@app.get("/api/config")
def get_config():
    cfg = build_settings()
    return ConfigResponse(models=MODEL_REGISTRY, current_settings=cfg)

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if req.model_key not in MODEL_REGISTRY:
        raise HTTPException(400, f"Model '{req.model_key}' tidak dikenal. Pilihan: {list(MODEL_REGISTRY.keys())}")
    model_type = MODEL_REGISTRY[req.model_key][1]
    if model_type == "online" and not req.api_key:
        raise HTTPException(400, "Model online membutuhkan API Key")
    try:
        result = workflow.run(req.question, req.model_key, req.api_key)
        return ChatResponse(answer=result["answer"], sources=result["sources"], latency_ms=result["latency_ms"])
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/chat/stream")
def chat_stream(req: ChatRequest):
    if req.model_key not in MODEL_REGISTRY:
        raise HTTPException(400, f"Model '{req.model_key}' tidak dikenal")
    model_type = MODEL_REGISTRY[req.model_key][1]
    if model_type == "online" and not req.api_key:
        raise HTTPException(400, "Model online membutuhkan API Key")
    async def event_generator():
        try:
            docs = workflow.retrieve(req.question, k=req.k)
            context = "\n\n".join([d.page_content for d in docs])
            yield {"event": "sources", "data": json.dumps([d.metadata.get("source", f"Dok {i+1}") for i, d in enumerate(docs)])}
            t0 = time.time()
            prompt = f"""Kamu adalah asisten akademik Program Studi Sistem Informasi Universitas Trunojoyo Madura.
Jawab pertanyaan berdasarkan konteks di bawah ini.
Jika jawaban tidak ada di konteks, katakan 'Maaf, informasi tersebut tidak tersedia di database saya'.
Gunakan bahasa Indonesia yang natural dan informatif.

KONTEKS:
{context}

PERTANYAAN: {req.question}
JAWABAN:"""
            from rag_si_utm.llms import build_ollama_llm
            from rag_si_utm.llms.ollama_llm import MODEL_REGISTRY as MR
            model_type_inner = MR[req.model_key][1]
            if model_type_inner == "local":
                llm = build_ollama_llm(MR[req.model_key][0], req.temperature)
                chunks = []
                for chunk in llm.stream(prompt):
                    chunks.append(chunk.content)
                    yield {"event": "token", "data": chunk.content}
                answer = "".join(chunks)
            else:
                import google.generativeai as genai
                import openai
                model_actual = MR[req.model_key][0]
                if "gemini" in model_actual:
                    genai.configure(api_key=req.api_key)
                    m = genai.GenerativeModel(model_actual)
                    response = m.generate_content(prompt)
                    answer = response.text
                    yield {"event": "token", "data": answer}
                else:
                    client = openai.OpenAI(api_key=req.api_key)
                    r = client.chat.completions.create(model=model_actual, messages=[{"role": "user", "content": prompt}], temperature=req.temperature, stream=True)
                    answer = ""
                    for chunk in r:
                        if chunk.choices[0].delta.content:
                            answer += chunk.choices[0].delta.content
                            yield {"event": "token", "data": chunk.choices[0].delta.content}
            latency = int((time.time() - t0) * 1000)
            yield {"event": "done", "data": json.dumps({"latency_ms": latency})}
        except Exception as e:
            yield {"event": "error", "data": str(e)}
    return EventSourceResponse(event_generator())

class EvalRequest(BaseModel):
    questions: list[str]
    model_key: str
    api_key: str = ""
    k: int = 3

@app.post("/api/evaluate")
def evaluate(req: EvalRequest):
    results = []
    for q in req.questions:
        try:
            r = workflow.run(q, req.model_key, req.api_key)
            results.append({"question": q, "answer": r["answer"], "sources": r["sources"], "latency_ms": r["latency_ms"]})
        except Exception as e:
            results.append({"question": q, "error": str(e)})
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8765, reload=True)

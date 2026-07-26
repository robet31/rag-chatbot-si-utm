from langchain_ollama import ChatOllama

MODEL_REGISTRY = {
    "Qwen 2.5 7B (Local)": ("qwen2.5:7b", "local"),
    "Llama 3.1 8B (Local)": ("llama3.1:8b", "local"),
    "Phi-3 Mini 3.8B (Local)": ("phi3:mini", "local"),
    "Gemma 2 9B (Local)": ("gemma2:9b", "local"),
    "GPT-4o Mini (Online)": ("gpt-4o-mini", "online"),
    "Gemini 1.5 Flash (Online)": ("gemini-1.5-flash", "online"),
}


def build_ollama_llm(model_name: str = "qwen2.5:7b", temperature: float = 0.3):
    return ChatOllama(model=model_name, temperature=temperature)


def build_online_llm(model_key: str, api_key: str):
    model_actual = MODEL_REGISTRY[model_key][0]
    if "gpt" in model_actual:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return client
    elif "gemini" in model_actual:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_actual)
    return None

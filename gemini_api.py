import os
import json
import faiss
import numpy as np
import google.generativeai as genai
import markdown
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

INDEX_PATH = "index/faiss.index"
VETORES_JSON = "index/vetores.json"

with open(VETORES_JSON, "r", encoding="utf-8") as f:
    base_de_dados = json.load(f)

dim = len(base_de_dados[0]["embedding"])
index = faiss.IndexFlatL2(dim)

embeddings = np.array([item["embedding"] for item in base_de_dados], dtype="float32")
index.add(embeddings)

resposta_cache = {}

@lru_cache(maxsize=1000)
def gerar_embedding(texto):
    response = genai.embed_content(
        model="models/embedding-001",
        content=texto,
        task_type="retrieval_query"
    )
    return tuple(response["embedding"])

def buscar_chunks_relevantes(pergunta, top_k=5):
    emb_pergunta = np.array([gerar_embedding(pergunta)], dtype="float32")
    distancias, indices = index.search(emb_pergunta, top_k)
    return [base_de_dados[i]["texto"] for i in indices[0]]

def gerar_resposta(pergunta, _contexto=None):
    if pergunta in resposta_cache:
        return resposta_cache[pergunta]
    
    try:
        contexto = "\n".join(buscar_chunks_relevantes(pergunta))
        prompt = (
            f"Você é um assistente de saúde e bem-estar. Responda à pergunta abaixo com confiança, "
            f"clareza e em tom natural, como se estivesse conversando diretamente com o usuário. "
            f"Não cite fontes ou diga que está se baseando em um texto."
            f"Use apenas as informações a seguir:\n\n{contexto}\n\nPergunta: {pergunta}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt)

        texto = resposta.text.strip().lower()

        termos_fora_do_tema = [
            "não contém", "não menciona", "não mencionei", "não encontrei", "não fala sobre",
            "não aborda", "não há informação", "não foi encontrado", "não está no texto",
            "não está disponível", "não encontrei nada sobre", "não está presente no texto",
            "não consigo responder", "política"
        ]
        if any(termo in texto for termo in termos_fora_do_tema):
            return None

        html_formatado = markdown.markdown(resposta.text.strip())
        resposta_cache[pergunta] = html_formatado
        return html_formatado
    
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta: {str(e)}"
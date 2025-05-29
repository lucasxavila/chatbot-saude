import os
import json
import google.generativeai as genai
import numpy as np
import markdown
from dotenv import load_dotenv

load_dotenv()  # Carrega a chave da API do .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Carrega embeddings
with open("index/vetores.json", "r", encoding="utf-8") as f:
    base_de_dados = json.load(f)

# Função para gerar embedding da pergunta
def gerar_embedding(texto):
    response = genai.embed_content(
        model="models/embedding-001",
        content=texto,
        task_type="retrieval_query"
    )
    return response["embedding"]

# Cálculo de similaridade (cosseno)
def similaridade(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Busca os chunks mais similares
def buscar_chunks_relevantes(pergunta, top_k=5):
    emb_pergunta = gerar_embedding(pergunta)
    similares = sorted(base_de_dados, key=lambda x: similaridade(x["embedding"], emb_pergunta), reverse=True)
    return [item["texto"] for item in similares[:top_k]]

def gerar_resposta(pergunta, _contexto=None):
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

        # Converte Markdown para html
        html_formatado = markdown.markdown(resposta.text.strip())

        return html_formatado
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta: {str(e)}"
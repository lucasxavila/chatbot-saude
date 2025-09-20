import os
import json
import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from processamento import extrair_textos_pdfs

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

VETORES_JSON = "index/vetores.json"
FAISS_INDEX = "index/faiss.index"

def dividir_em_chunks(texto, tamanho=500, overlap=50):
    """
    Divide o texto em pedaços (chunks) de até 'tamanho' caracteres,
    com sobreposição (overlap) para não cortar ideias no meio.
    """
    chunks = []
    start = 0
    while start < len(texto):
        end = start + tamanho
        chunk = texto[start:end]
        chunks.append(chunk)
        start += tamanho - overlap
    return chunks

def gerar_embedding(texto):
    """
    Gera embedding de um chunk de texto.
    """
    response = genai.embed_content(
        model="models/embedding-001",
        content=texto,
        task_type="retrieval_document"
    )
    return response["embedding"]

print("📄 Extraindo textos dos PDFs...")
texto = extrair_textos_pdfs([
    "material/saude_bem_estar_0.pdf",
    "material/saude_bem_estar_1.pdf",
    "material/saude_bem_estar_2.pdf",
    "material/saude_bem_estar_3.pdf"
])

print("✂️ Dividindo em chunks...")
chunks = dividir_em_chunks(texto, tamanho=500, overlap=50)

print("⚙️ Gerando embeddings...")
vetores = []
embeddings = []
for chunk in chunks:
    emb = gerar_embedding(chunk)
    vetores.append({"texto": chunk, "embedding": emb})
    embeddings.append(emb)

embeddings = np.array(embeddings, dtype="float32")

os.makedirs("index", exist_ok=True)

with open(VETORES_JSON, "w", encoding="utf-8") as f:
    json.dump(vetores, f, ensure_ascii=False)

print("📦 Criando índice FAISS...")
dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, FAISS_INDEX)

print(f"✅ Indexação concluída! Salvo em:\n - {VETORES_JSON}\n - {FAISS_INDEX}")

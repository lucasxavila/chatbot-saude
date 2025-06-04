import os
import json
from dotenv import load_dotenv
from processamento import extrair_textos_pdfs
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

embedding_model = genai.embed_content

def dividir_em_chunks(texto, tamanho=500):
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]

texto = extrair_textos_pdfs([
    "material/saude_bem_estar.pdf_0",
    "material/saude_bem_estar_1.pdf",
    "material/saude_bem_estar_2.pdf",
    "material/saude_bem_estar_3.pdf"
])
chunks = dividir_em_chunks(texto)

vetores = []
for chunk in chunks:
    response = embedding_model(
        model="models/embedding-001",
        content=chunk,
        task_type="retrieval_document"
    )
    vetores.append({
        "texto": chunk,
        "embedding": response["embedding"]
    })

os.makedirs("index", exist_ok=True)
with open("index/vetores.json", "w", encoding="utf-8") as f:
    json.dump(vetores, f, ensure_ascii=False)
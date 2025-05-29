from flask import Flask, render_template, request, jsonify
from processamento import extrair_textos_pdfs, extrair_intencao
from gemini_api import configurar_gemini, gerar_resposta
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

pdf_texto = extrair_textos_pdfs([
    "material/saude_bem_estar.pdf",
    "material/saude_bem_estar_1.pdf",
    "material/saude_bem_estar_2.pdf"
])
api_key = os.getenv("GEMINI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json()
    pergunta = dados["mensagem"].strip().lower()

    # Verifica se é uma saudação
    if pergunta in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]:
        resposta = "Olá, sou o chatbot BemViver! No que posso ajudar?"
    else:
        resposta = gerar_resposta(pergunta, pdf_texto)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
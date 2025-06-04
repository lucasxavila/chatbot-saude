from flask import Flask, render_template, request, jsonify
from processamento import extrair_textos_pdfs
from gemini_api import gerar_resposta
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

pdf_texto = extrair_textos_pdfs([
    "material/saude_bem_estar_0.pdf",
    "material/saude_bem_estar_1.pdf",
    "material/saude_bem_estar_2.pdf",
    "material/saude_bem_estar_3.pdf"
])
api_key = os.getenv("GEMINI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json()
    pergunta = dados["mensagem"].strip().lower()

    saudacoes = ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]
    despedidas = ["tchau", "até mais", "adeus", "obrigado", "obrigada", "valeu", "até", "até logo", "até breve", "flw", "falou", "encerrar", "fim"]

    if pergunta in saudacoes:
        resposta = "Olá, sou o chatbot BemViver! No que posso ajudar?"
    elif any(despedida in pergunta for despedida in despedidas):
        resposta = "Foi um prazer te ajudar! Se precisar de mais alguma coisa, estarei por aqui."
    else:
        resposta = gerar_resposta(pergunta, pdf_texto)
        if not resposta:
            resposta = "Não tenho informações sobre isso! Sou um chatbot de saúde e bem-estar. Posso te ajudar com algo nesse tema?"
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
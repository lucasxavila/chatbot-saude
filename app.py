from flask import Flask, render_template, request, jsonify
from processamento import extrair_texto_pdf, extrair_intencao
from gemini_api import configurar_gemini, gerar_resposta
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

pdf_texto = extrair_texto_pdf("material/saude_bem_estar.pdf")
api_key = os.getenv("GEMINI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json()
    pergunta = dados["mensagem"]
    resposta = gerar_resposta(pergunta, pdf_texto)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
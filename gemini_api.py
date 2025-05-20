import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Carrega a chave da API do .env

def configurar_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave da API GEMINI_API_KEY não foi encontrada no arquivo .env.")
    genai.configure(api_key=api_key)

def gerar_resposta(pergunta, contexto_pdf):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            f"Com base neste conteúdo:\n\n{contexto_pdf[:10000]}\n\nResponda à pergunta:\n{pergunta}"
        )
        return response.text
    except Exception as e:
        # Log da exceção pode ser feito aqui se desejar (ex: via print ou log)
        return f"Ocorreu um erro ao gerar a resposta. Detalhes técnicos: {str(e)}"
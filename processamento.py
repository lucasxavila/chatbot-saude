import fitz
import spacy

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    return texto

nlp = spacy.load("pt_core_news_sm")

def extrair_intencao(texto_usuario):
    doc = nlp(texto_usuario.lower())
    if "alimentação" in texto_usuario:
        return "alimentacao"
    elif "exercício" in texto_usuario or "atividade física" in texto_usuario:
        return "exercicio"
    elif "sono" in texto_usuario:
        return "sono"
    else:
        return "geral"
import fitz
import spacy

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    return texto

def extrair_textos_pdfs(lista_caminhos_pdf):
    texto_total = ""
    for caminho in lista_caminhos_pdf:
        texto_total += extrair_texto_pdf(caminho) + "\n"
    return texto_total

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
import fitz

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
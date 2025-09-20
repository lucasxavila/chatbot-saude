# Chatbot BemViver: Saúde e Bem-Estar

Este é um projeto de chatbot interativo voltado para temas de saúde e bem-estar, construído com Python e Flask no backend, e HTML, CSS e JavaScript no frontend. O chatbot utiliza a **Gemini API** para processar e responder perguntas dos usuários, além da técnica de PLN - embeddings.

Com as últimas melhorias, o chatbot agora conta com cache de respostas e busca semântica otimizada com FAISS, o que torna as respostas mais rápidas e eficientes, especialmente para perguntas repetidas ou similares.

## Demonstração

<img width="750" height="877" alt="image" src="https://github.com/user-attachments/assets/16248443-8a08-4a79-baa3-580e25316a4c" />

Interface web simples onde o usuário pode digitar perguntas apenas relacionadas à saúde e receber respostas instantâneas.

Link demonstrando o funcionamento do Chatbot: <a href="https://youtu.be/z3RBn8antK0">https://youtu.be/z3RBn8antK0</a>

## Tecnologias Utilizadas

- Python 3.11
- Flask
- HTML, CSS, JavaScript
- Gemini API
- FAISS (busca semântica rápida)
- Gunicorn (para deploy no Railway)
- Werkzeug
- Jinja2

## Estrutura do Projeto

`chatbot_saude/`  
`app.py:` Roteamento Flask e interface principal do chatbot  
`gemini_api.py:` Conexão com a API da Gemini  
`indexador_gemini.py:` Indexação de informações para contexto das respostas  
`processamento.py:` Processamento de perguntas e formatação de respostas  
`templates/`  
`index.html:` Interface HTML principal  
`static/`  
`style.css:` Estilo HTML  
`script.js:` Responsável por interatividade, como enviar perguntas para o backend  
`requirements.txt:` Dependências do projeto  
`Procfile:` Arquivo para deploy no Railway  
`README.md`

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucasxavila/chatbot-saude.git
2. Navegue até o diretório do projeto:
   ```bash
   cd chatbot-saude
3. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv\Scripts\activate
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
5. Configure sua chave da API Gemini em um arquivo ```.env```, com a variável:
   ```bash
   GEMINI_API_KEY=sua-chave
7. Execute a aplicação:
   ```bash
   python app.py

## Deploy
O projeto está configurado para deploy no Railway usando Procfile e runtime.txt.

### Funcionalidades
- Interface web simples e responsiva;
- Integração com a Gemini API para respostas contextuais;
- Cache de respostas para perguntas repetidas → respostas instantâneas;
- Busca semântica otimizada com FAISS → pesquisa rápida nos dados indexados;
- Indexação e pré-processamento de dados para respostas mais precisas;
- Estrutura modular para facilitar manutenções e melhorias.

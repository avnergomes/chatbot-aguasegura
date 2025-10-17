# 💧 Chatbot Água Segura

Aplicativo Streamlit que demonstra como criar um chatbot especializado no Programa Água Segura utilizando a API da OpenAI e documentos de referência locais.

## Como executar localmente

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Defina a chave da OpenAI. O método mais seguro é criar o arquivo `.streamlit/secrets.toml` com o conteúdo:

   ```toml
   OPENAI_API_KEY = "sua-chave"
   ```

   Também é possível definir a variável de ambiente `OPENAI_API_KEY` ou informar a chave diretamente na interface quando solicitado.

3. Adicione os materiais de apoio exportados do drive na pasta `data/references`. O aplicativo aceita arquivos `.md` e `.txt` e eles serão incorporados automaticamente ao contexto do chatbot.

4. Inicie o aplicativo:

   ```bash
   streamlit run streamlit_app.py
   ```

## Estrutura da base de conhecimento

- `data/knowledge_base.py`: contém o resumo oficial do programa e agrega automaticamente os arquivos presentes em `data/references`.
- `data/document_loader.py`: utilitário para carregar os documentos locais em memória.
- `data/references/`: diretório onde devem ser armazenados os materiais de referência (por exemplo, guias, manuais, planilhas exportadas como texto).

O conteúdo desses arquivos é exibido na barra lateral da aplicação e usado para montar a mensagem de sistema enviada ao modelo.

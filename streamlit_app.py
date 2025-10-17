import os
from typing import Dict, List

import streamlit as st
from openai import OpenAI

from data.document_loader import load_reference_documents
from data.knowledge_base import BASE_GUIDE, PROGRAM_KNOWLEDGE


st.set_page_config(page_title="Chatbot Água Segura", page_icon="💧")

st.title("💧 Chatbot Água Segura")
st.write(
    "Este assistente foi treinado com diretrizes do Programa Água Segura para apoiar técnicos, "
    "produtores rurais, gestores públicos e demais parceiros. Faça perguntas sobre diagnósticos, "
    "infraestrutura, monitoramento ou mobilização social e receba orientações contextualizadas."
)
st.caption(
    "💡 Dica: armazene sua chave em `.streamlit/secrets.toml` como `OPENAI_API_KEY` ou defina a "
    "variável de ambiente correspondente para evitar digitá-la manualmente."
)


def get_api_key() -> str:
    """Recupera a chave da API da OpenAI do secrets, variável de ambiente ou entrada manual."""
    secret_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
    env_key = os.getenv("OPENAI_API_KEY")

    if secret_key:
        return secret_key
    if env_key:
        return env_key

    return st.text_input("OpenAI API Key", type="password")


def build_system_prompt() -> str:
    """Constrói a mensagem de sistema com o conhecimento do programa."""
    return (
        "Você é o Assistente Água Segura, um especialista em segurança hídrica, saneamento rural e "
        "gestão comunitária. Utilize exclusivamente as informações fornecidas abaixo para orientar "
        "técnicos municipais, produtores rurais e stakeholders. Quando não houver informação disponível, "
        "admita explicitamente a limitação e sugira consultar a coordenação do programa.\n\n"
        f"Base de conhecimento oficial:\n{PROGRAM_KNOWLEDGE.strip()}"
    )


def render_messages(messages: List[Dict[str, str]]) -> None:
    """Renderiza as mensagens na interface de chat."""
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_sidebar(reference_docs: Dict[str, str]) -> None:
    """Render the contextual help sidebar with program references."""
    with st.sidebar:
        st.header("Base de conhecimento")
        st.caption(
            "Os documentos abaixo vêm do diretório `data/references`. "
            "Adicione os arquivos exportados do drive (formato .md ou .txt) para "
            "que o assistente utilize as informações mais atualizadas."
        )

        if not reference_docs:
            st.info(
                "Nenhum documento foi encontrado. Coloque os materiais de apoio "
                "no diretório indicado e recarregue o aplicativo.",
                icon="📁",
            )
            st.markdown("---")
            st.markdown("### Resumo oficial")
            st.markdown(BASE_GUIDE)
            return

        options = ["Resumo oficial do programa", *sorted(reference_docs.keys())]
        selected = st.selectbox("Consultar material de apoio", options=options, index=0)

        if selected == "Resumo oficial do programa":
            st.markdown("### Resumo oficial")
            st.markdown(BASE_GUIDE)
            return

        st.markdown(f"### {selected}")
        st.markdown(reference_docs[selected])


def main() -> None:
    api_key = get_api_key()

    if not api_key:
        st.info("Informe a chave da API da OpenAI para continuar.", icon="🗝️")
        return

    client = OpenAI(api_key=api_key)
    reference_docs = load_reference_documents()

    render_sidebar(reference_docs)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": build_system_prompt()},
            {
                "role": "assistant",
                "content": (
                    "Olá! Estou pronto para ajudar com ações do Programa Água Segura."
                    " Pergunte sobre planejamento, tecnologias de tratamento, monitoramento"
                    " participativo ou indicadores de sucesso."
                ),
            },
        ]

    render_messages(
        [message for message in st.session_state.messages if message["role"] != "system"]
    )

    if prompt := st.chat_input("Envie sua pergunta"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=0.2,
            )
            response_text = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()

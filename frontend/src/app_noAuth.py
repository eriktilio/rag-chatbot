import streamlit as st
import time
from service import rag_service


# --- Configuração da Página ---
st.set_page_config(
    page_title="Chatbot com RAG",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ================================
# SIDEBAR – Gerenciamento de PDFs
# ================================
with st.sidebar:
    st.header("Gerenciamento de Documentos")

    # ------------------------------
    # Upload de PDF
    # ------------------------------
    with st.expander("📤 Upload de PDF", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecione um arquivo PDF para adicionar à base de conhecimento.",
            type="pdf"
        )

        if st.button("Processar e Indexar"):
            if uploaded_file:
                with st.spinner("Processando e indexando o arquivo..."):
                    result = rag_service.upload_file(uploaded_file)

                    if result and "error" not in result:
                        st.success(f"Arquivo '{result.get('file')}' indexado com sucesso!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"Erro: {result.get('error')}")
            else:
                st.warning("Por favor, selecione um arquivo PDF.")

    # ------------------------------
    # Lista de arquivos indexados
    # ------------------------------
    st.header("📄 Arquivos Indexados")

    indexed_files = rag_service.get_indexed_files()

    if not indexed_files or isinstance(indexed_files, dict) and "error" in indexed_files:
        st.info("Nenhum documento indexado. Faça o upload de um PDF para começar.")
    else:
        for file_name in indexed_files:
            col1, col2 = st.columns([0.8, 0.2])

            with col1:
                st.text(file_name)

            with col2:
                if st.button("🗑️", key=f"delete_{file_name}", help=f"Deletar {file_name}"):
                    with st.spinner(f"Deletando {file_name}..."):
                        rag_service.delete_file(file_name)
                        st.success(f"Arquivo '{file_name}' deletado.")
                        time.sleep(2)
                        st.rerun()


# ================================
# CHAT PRINCIPAL
# ================================
st.title("🤖 Chatbot com RAG")
st.caption("Faça perguntas sobre os documentos que você indexou.")


# Histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []


# Exibe mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Campo de entrada para o usuário
if prompt := st.chat_input("Qual a sua dúvida?"):

    # Armazena e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do modelo RAG
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("Pensando..."):
            result = rag_service.query_rag(prompt)

            if result and "answer" in result:
                full_response = result["answer"]
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            else:
                full_response = (
                    "Não foi possível obter uma resposta. "
                    "Verifique se a API está online e se há documentos indexados."
                )

        message_placeholder.markdown(full_response)

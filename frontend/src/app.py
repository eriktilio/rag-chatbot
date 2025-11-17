import streamlit as st
from service import rag_service
from login import show_login_page, logout
from admin import show_admin_page


# --- Configuração da Página ---
st.set_page_config(
    page_title="Chatbot com RAG",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Gerenciamento de Estado da Página ---
if "page" not in st.session_state:
    st.session_state["page"] = "chat"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ================================
# SIDEBAR – Navegação
# ================================
with st.sidebar:
    st.header("Navegação")
    if st.session_state["authenticated"]:
        st.sidebar.button("Sair", on_click=logout)
        if st.button("Área Administrativa"):
            st.session_state["page"] = "admin"
            #st.rerun()
    else:
        if st.button("Área Administrativa"):
            st.session_state["page"] = "login"
            #st.rerun()
        if st.button("Chat"):
            st.session_state["page"] = "chat"
            #st.rerun()

# ================================
# Roteamento de Páginas
# ================================
if st.session_state["page"] == "login":
    show_login_page()

elif st.session_state["page"] == "admin":
    if st.session_state["authenticated"]:
        show_admin_page()
    else:
        st.warning("Você precisa estar logado para acessar esta página.")
        show_login_page()

elif st.session_state["page"] == "chat":
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

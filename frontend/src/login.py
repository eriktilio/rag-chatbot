import streamlit as st

def show_login_page():
    """Exibe a página de login e gerencia a autenticação."""
    st.header("Área Administrativa - Login")

    # --- Mock de credenciais ---
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "admin"

    # --- Campos de login ---
    username = st.text_input("Usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["page"] = "admin"  # Redireciona para a página de admin
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def logout():
    """Realiza o logout do usuário."""
    if "authenticated" in st.session_state:
        del st.session_state["authenticated"]
    st.session_state["page"] = "chat"  # Redireciona para a página de chat
    #st.rerun()

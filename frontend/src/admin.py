import streamlit as st
import time
import os
from service import rag_service

# This should be in a more secure place in a real app
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"

def show_login_page():
    """Shows the login form and handles authentication."""
    st.header("Área Administrativa - Login")

    username = st.text_input("Usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def show_admin_page():
    """Shows the document management interface."""
    st.header("Gerenciamento de Documentos")
    
    if st.button("Sair"):
        st.session_state["authenticated"] = False
        st.rerun()

    with st.expander("📄 Exemplo de Formato de Arquivo", expanded=False):
        st.markdown("""
        O arquivo PDF a ser indexado deve seguir uma estrutura de títulos e parágrafos para uma melhor organização e recuperação da informação. 
        
        **Estrutura Recomendada:**

        - **Título do Documento (ou Seção Principal):** Use um estilo de título grande e centralizado.
        - **Subtítulos:** Use estilos de título menores para as seções secundárias.
        - **Parágrafos:** O conteúdo de texto normal sob cada título.

        Abaixo, um botão para baixar um arquivo de exemplo:
        """)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_pdf_path = os.path.join(script_dir, "sample.pdf")

        if os.path.exists(sample_pdf_path):
            with open(sample_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Baixar PDF de Exemplo",
                    data=pdf_file,
                    file_name="sample.pdf",
                    mime="application/octet-stream"
                )
        else:
            st.warning("Arquivo de exemplo (sample.pdf) não encontrado.")

    with st.expander("📤 Upload de PDF", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecione um arquivo PDF para adicionar à base de conhecimento.",
            type="pdf"
        )
        if st.button("Processar e Indexar", key="processar_button"):
            if uploaded_file:
                with st.spinner("Processando e indexando o arquivo..."):
                    try:
                        result = rag_service.upload_file(uploaded_file)
                        if result and "error" not in result:
                            st.success(f"Arquivo '{result.get('file')}' indexado com sucesso!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"Erro: {result.get('error', 'Erro desconhecido.')}")
                    except Exception as e:
                        st.error(f"Falha ao conectar com o serviço de upload: {e}")
            else:
                st.warning("Por favor, selecione um arquivo PDF.")

    st.header("📄 Arquivos Indexados")
    try:
        indexed_files = rag_service.get_indexed_files()
        if not indexed_files or (isinstance(indexed_files, dict) and "error" in indexed_files):
            st.info("Nenhum documento indexado. Faça o upload de um PDF para começar.")
        else:
            for file_name in indexed_files:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.text(file_name)
                with col2:
                    if st.button("🗑️", key=f"delete_{file_name}", help=f"Deletar {file_name}"):
                        with st.spinner(f"Deletando {file_name}..."):
                            try:
                                rag_service.delete_file(file_name)
                                st.success(f"Arquivo '{file_name}' deletado.")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Falha ao deletar o arquivo: {e}")
    except Exception as e:
        st.error(f"Não foi possível buscar os arquivos indexados. Verifique a API. Erro: {e}")

# --- Main Logic for Admin Page ---
st.set_page_config(page_title="Admin", page_icon="⚙️", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    show_admin_page()
else:
    show_login_page()

import streamlit as st
import time
from service import rag_service
from login import logout

def show_admin_page():
    """Exibe a página de administração para gerenciar documentos."""
    st.header("Gerenciamento de Documentos")
    
    # CORREÇÃO: Adicionada uma 'key' única para este botão da sidebar
    # Isso evita conflito com qualquer outro botão "Sair" em outra página.
    #st.sidebar.button("Sair", on_click=logout, key="admin_logout_button")

    # ------------------------------
    # Upload de PDF
    # ------------------------------
    with st.expander("📤 Upload de PDF", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecione um arquivo PDF para adicionar à base de conhecimento.",
            type="pdf"
        )

        # BOA PRÁTICA: Adicionada uma 'key' aqui também
        if st.button("Processar e Indexar", key="processar_button"):
            if uploaded_file:
                with st.spinner("Processando e indexando o arquivo..."):
                    result = rag_service.upload_file(uploaded_file)

                    if result and "error" not in result:
                        st.success(f"Arquivo '{result.get('file')}' indexado com sucesso!")
                        time.sleep(2)
                        #st.rerun()
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
                # Esta parte já estava correta, pois usava uma key dinâmica!
                if st.button("🗑️", key=f"delete_{file_name}", help=f"Deletar {file_name}"):
                    with st.spinner(f"Deletando {file_name}..."):
                        rag_service.delete_file(file_name)
                        st.success(f"Arquivo '{file_name}' deletado.")
                        time.sleep(2)
                        #st.rerun()
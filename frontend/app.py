import streamlit as st
import requests
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="Chatbot com RAG",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Constantes ---
API_URL = "http://127.0.0.1:8000"  # URL base da sua API FastAPI

# --- Funções de Interação com a API ---

def get_indexed_files():
    """Busca a lista de arquivos PDF indexados."""
    try:
        response = requests.get(f"{API_URL}/files")
        response.raise_for_status()
        return response.json().get("uploaded_pdfs", [])
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Erro ao conectar à API: {e}")
        return []

def upload_file(file):
    """Envia um arquivo PDF para a API para ser indexado."""
    files = {"file": (file.name, file.getvalue(), file.type)}
    try:
        response = requests.post(f"{API_URL}/upload", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Falha no upload: {e}")
        return None

def delete_file(filename):
    """Solicita a remoção de um arquivo do índice."""
    try:
        response = requests.delete(f"{API_URL}/files/{filename}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Falha ao deletar: {e}")
        return None

def query_rag(question):
    """Envia uma pergunta para o modelo RAG."""
    try:
        response = requests.post(f"{API_URL}/query", json={"question": question})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao consultar o modelo: {e}")
        return None

# --- Interface do Usuário (Sidebar) ---

with st.sidebar:
    st.header("Gerenciamento de Documentos")

    # Seção de Upload
    with st.expander("📤 Upload de PDF", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecione um arquivo PDF para adicionar à base de conhecimento.", type="pdf"
        )
        if st.button("Processar e Indexar"):
            if uploaded_file:
                with st.spinner("Processando e indexando o arquivo..."):
                    result = upload_file(uploaded_file)
                    if result:
                        st.success(f"Arquivo '{result.get('file')}' indexado com sucesso!")
                        time.sleep(2) # Pausa para o usuário ver a mensagem
                        st.rerun()
            else:
                st.warning("Por favor, selecione um arquivo PDF.")

    # Seção de Arquivos Indexados
    st.header("📄 Arquivos Indexados")
    indexed_files = get_indexed_files()

    if not indexed_files:
        st.info("Nenhum documento indexado. Faça o upload de um PDF para começar.")
    else:
        for file_name in indexed_files:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.text(file_name)
            with col2:
                if st.button("🗑️", key=f"delete_{file_name}", help=f"Deletar {file_name}"):
                    with st.spinner(f"Deletando {file_name}..."):
                        delete_file(file_name)
                        st.success(f"Arquivo '{file_name}' deletado.")
                        time.sleep(2)
                        st.rerun()


# --- Interface Principal do Chat ---

st.title("🤖 Chatbot com RAG")
st.caption("Faça perguntas sobre os documentos que você indexou.")

# Inicialização do histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Qual a sua dúvida?"):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera e exibe a resposta do bot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner("Pensando..."):
            result = query_rag(prompt)
            if result and "answer" in result:
                full_response = result["answer"]
                # Adiciona a resposta do bot ao histórico
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                full_response = "Não foi possível obter uma resposta. Verifique se a API está online e se há documentos indexados."

        message_placeholder.markdown(full_response)

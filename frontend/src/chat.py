import streamlit as st
from service import rag_service

st.set_page_config(page_title="Chat", page_icon="🤖", layout="centered")

st.title("🤖 Chatbot com RAG")
st.caption("Faça perguntas sobre os documentos que você indexou.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Qual a sua dúvida?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Pensando..."):
            try:
                result = rag_service.query_rag(prompt)
                if result and "answer" in result:
                    full_response = result["answer"]
                else:
                    full_response = "Não foi possível obter uma resposta. Verifique a API."
            except Exception as e:
                full_response = f"Ocorreu um erro ao contatar o serviço: {e}"
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

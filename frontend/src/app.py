import streamlit as st

st.set_page_config(
    page_title="Chatbot com RAG",
    page_icon="🤖",
    layout="centered",
)

pages = [
    st.Page("chat.py", title="Chat", icon="🤖", default=True),
    st.Page("admin.py", title="Admin", icon="⚙️"),
]

pg = st.navigation(pages, position="top")

pg.run()

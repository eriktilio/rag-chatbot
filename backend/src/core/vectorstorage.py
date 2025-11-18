from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config import EMBEDDING_MODEL_NAME, VECTORSTORE_PATH
import os


def get_embeddings():
    """Retorna o modelo de embeddings do Hugging Face."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def load_vectorstore():
    """Carrega o índice FAISS corretamente."""
    if not os.path.exists(VECTORSTORE_PATH):
        return None

    embeddings = get_embeddings()

    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,  # necessário para HFEmbeddings
    )


def save_vectorstore(vs):
    """Salva a vectorstore FAISS corretamente."""
    vs.save_local(VECTORSTORE_PATH)


def add_documents(docs):
    """Adiciona documentos ao índice FAISS."""
    embeddings = get_embeddings()
    vs = load_vectorstore()

    if vs is None:
        vs = FAISS.from_documents(docs, embeddings)
    else:
        vs.add_documents(docs)

    save_vectorstore(vs)


def get_retriever(k=4):
    """Retorna um retriever para busca semântica."""
    vs = load_vectorstore()
    if vs is None:
        raise ValueError("Nenhum vetor armazenado ainda.")
    return vs.as_retriever(search_kwargs={"k": k})


def delete_document(filename: str):
    """Remove vetores associados a um PDF identificado pelo campo metadata['source']."""    
    vs = load_vectorstore()

    if vs is None:
        raise ValueError("Nenhum vetor armazenado ainda.")

    # Filtra apenas os documentos cujo source NÃO seja o arquivo a excluir
    remaining_docs = [
        doc for doc in vs.docstore._dict.values()
        if doc.metadata.get("source") != filename
    ]

    # Nenhum documento foi removido → arquivo inexistente
    if len(remaining_docs) == len(vs.docstore._dict):
        raise ValueError(f"Arquivo '{filename}' não encontrado no índice.")

    # 🔥 Caso não reste nenhum documento → resetar FAISS
    if not remaining_docs:
        import shutil
        shutil.rmtree(VECTORSTORE_PATH, ignore_errors=True)
        return

    # Recria FAISS com os documentos restantes
    embeddings = get_embeddings()

    new_vs = FAISS.from_documents(remaining_docs, embeddings)
    save_vectorstore(new_vs)


def list_documents():
    """Lista todos os arquivos PDF indexados."""
    vs = load_vectorstore()
    if vs is None:
        return []

    return list({
        doc.metadata.get("source", "desconhecido")
        for doc in vs.docstore._dict.values()
    })

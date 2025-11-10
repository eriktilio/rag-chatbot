from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config import EMBEDDING_MODEL_NAME, VECTORSTORE_PATH
import os
import pickle


def get_embeddings():
    """
    Cria e retorna o modelo de embeddings do Hugging Face.

    Returns:
        HuggingFaceEmbeddings: Objeto de embeddings configurado.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def load_vectorstore():
    """
    Carrega o índice vetorial FAISS salvo em disco, se existir.

    Returns:
        FAISS | None: O índice carregado ou None se não existir.
    """
    if os.path.exists(VECTORSTORE_PATH):
        with open(VECTORSTORE_PATH, "rb") as f:
            return pickle.load(f)
    return None


def save_vectorstore(vs):
    """
    Salva o índice vetorial FAISS no disco.

    Args:
        vs (FAISS): O índice vetorial a ser salvo.
    """
    with open(VECTORSTORE_PATH, "wb") as f:
        pickle.dump(vs, f)


def add_documents(docs):
    """
    Adiciona novos documentos ao índice FAISS existente
    ou cria um novo índice se ainda não existir.

    Args:
        docs (list[Document]): Lista de documentos a serem indexados.
    """
    embeddings = get_embeddings()
    vs = load_vectorstore()
    if vs:
        vs.add_documents(docs)
    else:
        vs = FAISS.from_documents(docs, embeddings)
    save_vectorstore(vs)


def get_retriever(k=4):
    """
    Retorna um retriever para busca semântica no índice FAISS.

    Args:
        k (int, optional): Quantidade de resultados a retornar. Default é 4.

    Returns:
        BaseRetriever: Um retriever configurado.
    
    Raises:
        ValueError: Se o índice ainda não foi criado.
    """
    vs = load_vectorstore()
    if not vs:
        raise ValueError("Nenhum vetor armazenado ainda.")
    return vs.as_retriever(search_kwargs={"k": k})


def delete_document(filename: str):
    """
    Remove todos os vetores associados a um PDF específico
    (identificado pelo campo metadata['source']).

    Args:
        filename (str): Nome do arquivo PDF a ser removido.

    Raises:
        ValueError: Se o índice não existir ou o arquivo não for encontrado.
    """
    vs = load_vectorstore()
    if not vs:
        raise ValueError("Nenhum vetor armazenado ainda.")

    # Filtra documentos que não pertencem ao arquivo
    new_docs = [doc for doc in vs.docstore._dict.values() if doc.metadata.get("source") != filename]

    if len(new_docs) == len(vs.docstore._dict):
        raise ValueError(f"Arquivo '{filename}' não encontrado no índice.")

    embeddings = get_embeddings()
    new_vs = FAISS.from_documents(new_docs, embeddings)
    save_vectorstore(new_vs)


def list_documents():
    """
    Lista todos os PDFs que já foram carregados e indexados.

    Returns:
        list[str]: Lista com nomes dos arquivos PDF no índice.
    """
    vs = load_vectorstore()
    if not vs:
        return []
    return list({doc.metadata.get("source", "desconhecido") for doc in vs.docstore._dict.values()})

from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config import EMBEDDING_MODEL_NAME

def get_embeddings():
    """
    Cria e retorna o modelo de embeddings do Hugging Face definido nas configurações.

    Returns:
        HuggingFaceEmbeddings: Objeto de embeddings configurado para gerar vetores semânticos.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

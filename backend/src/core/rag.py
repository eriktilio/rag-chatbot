from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ..config import GEMINI_MODEL, GOOGLE_API_KEY


def build_rag_chain(retriever):
    """
    Constrói uma pipeline RAG (Retrieval-Augmented Generation) usando um retriever
    e o modelo ChatGoogleGenerativeAI para gerar respostas baseadas em contexto.

    Esta função retorna uma função interna `rag_pipeline` que recebe uma pergunta,
    recupera documentos relevantes, formata o prompt com o contexto, envia para o
    modelo LLM e retorna a resposta junto com os metadados dos documentos usados.

    Args:
        retriever (BaseRetriever): Objeto responsável por recuperar documentos relevantes
            do índice vetorial FAISS ou outro vectorstore.

    Returns:
        Callable[[str], dict]: Função que recebe uma pergunta (str) e retorna um
            dicionário com as chaves:
                - "question": a pergunta original.
                - "answer": resposta gerada pelo modelo.
                - "context_docs": lista de metadados dos documentos usados.
    """

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0.0,
        google_api_key=GOOGLE_API_KEY,
    )
    
    prompt = ChatPromptTemplate.from_template(
        "Você é um assistente útil. Use o contexto abaixo para responder de forma clara e objetiva.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta:\n{question}\n\n"
        "Resposta:"
    )

    def rag_pipeline(question: str):
        # Recupera documentos relevantes
        docs = retriever._get_relevant_documents(question, run_manager=None)

        # Concatena os conteúdos dos documentos
        context = "\n\n".join([doc.page_content for doc in docs])

        # Formata o prompt
        formatted_prompt = prompt.format(context=context, question=question)

        # Gera a resposta
        response = llm.invoke(formatted_prompt)

        # Retorna resultado estruturado
        return {
            "question": question,
            "answer": response.content,
            "context_docs": [doc.metadata for doc in docs],
        }


    return rag_pipeline

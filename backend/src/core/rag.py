from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ..config import GEMINI_MODEL, GOOGLE_API_KEY


def build_rag_chain(retriever):

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

        # Concatena o conteúdo dos documentos
        context = "\n\n".join([doc.page_content for doc in docs])

        # Formata prompt
        formatted_prompt = prompt.format(
            context=context,
            question=question
        )

        # Gera resposta
        response = llm.invoke(formatted_prompt)

        # Retorna documento COMPLETO (não só metadata)
        return {
            "question": question,
            "answer": response.content,
            "context_docs": [
                {
                    "source": doc.metadata.get("source"),
                    "content": doc.page_content
                }
                for doc in docs
            ],
        }

    return rag_pipeline

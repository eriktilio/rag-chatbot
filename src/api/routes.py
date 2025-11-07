from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from io import BytesIO
from pydantic import BaseModel
from ..core.vectorstorage import add_documents, get_retriever, list_documents, delete_document
from ..core.rag import build_rag_chain
from ..config import CHUNK_SIZE, CHUNK_OVERLAP

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    k: int = 4


# --- Endpoint de upload de Documentos ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Envie apenas arquivos PDF.")

    content = await file.read()
    reader = PdfReader(BytesIO(content))
    text = "\n".join([p.extract_text() or "" for p in reader.pages])

    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF sem texto legível.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    docs = [
        Document(page_content=chunk, metadata={"source": file.filename})
        for chunk in splitter.split_text(text)
    ]

    add_documents(docs)
    return {"status": "ok", "chunks": len(docs), "file": file.filename}


# --- Endpoint de consulta (RAG) ---
@router.post("/query")
async def query_rag(body: QueryRequest):
    """
    Endpoint para fazer uma pergunta ao modelo Gemini usando RAG.
    """
    try:
        retriever = get_retriever(body.k)
    except ValueError:
        raise HTTPException(status_code=400, detail="Nenhum documento indexado.")

    # Constrói a pipeline RAG
    rag_pipeline = build_rag_chain(retriever)

    # Executa a pipeline de forma síncrona (Gemini é síncrono, não precisa await)
    result = rag_pipeline(body.question)

    return {
        "question": body.question,
        "answer": result["answer"],
        "context_docs": result["context_docs"]
    }

# --- Endpoint de consulta de Documentos ---
@router.get("/files")
async def list_files():
    """Lista todos os PDFs carregados"""
    files = list_documents()
    return {"uploaded_pdfs": files}


# --- Endpoint de exclusão de Documentos ---
@router.delete("/files/{filename}")
async def remove_file(filename: str):
    """Remove um PDF do índice"""
    try:
        delete_document(filename)
        return {"status": "deleted", "file": filename}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
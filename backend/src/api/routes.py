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


# --- Endpoint de upload de documentos ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Envie apenas arquivos PDF.")

    # NORMALIZA O NOME DO ARQUIVO (evita problemas no delete)
    filename = file.filename.strip()

    content = await file.read()

    try:
        reader = PdfReader(BytesIO(content))
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao ler PDF. Arquivo pode estar corrompido.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF sem texto legível.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_text(text)

    docs = [
        Document(page_content=chunk, metadata={"source": filename})
        for chunk in chunks
    ]

    add_documents(docs)

    return {
        "status": "ok",
        "chunks": len(docs),
        "file": filename
    }


# --- Endpoint para consulta RAG ---
@router.post("/query")
async def query_rag(body: QueryRequest):
    try:
        retriever = get_retriever(body.k)
    except ValueError:
        raise HTTPException(status_code=400, detail="Nenhum documento indexado.")

    chain = build_rag_chain(retriever)
    result = chain(body.question)

    context_docs = [
        {
            "source": d.get("source"),
            "content": d.get("content")
        }
        for d in result.get("context_docs", [])
    ]

    return {
        "question": body.question,
        "answer": result.get("answer", ""),
        "context_docs": context_docs,
    }


# --- Endpoint de listagem ---
@router.get("/files")
async def list_files():
    files = list_documents()
    return {"uploaded_pdfs": files}


# --- Endpoint de exclusão ---
@router.delete("/files/{filename}")
async def remove_file(filename: str):
    filename = filename.strip()

    try:
        delete_document(filename)
        return {"status": "deleted", "file": filename}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

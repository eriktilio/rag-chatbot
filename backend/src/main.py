from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.routes import router
from .core.vectorstorage import load_vectorstore


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_vectorstore()
    yield


app = FastAPI(
    title="RAG CHATBOT API",
    lifespan=lifespan
)

# -------------------------------
# CORS CONFIG
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://frontend:8501",
        "http://localhost:8501"
        ],
    allow_credentials=True,
    allow_methods=["*"],           # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],           # Permite todos os headers
)

# Rotas
app.include_router(router)

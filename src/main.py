from fastapi import FastAPI
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

app.include_router(router)

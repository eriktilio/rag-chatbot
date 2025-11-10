import os
from dotenv import load_dotenv

# Carrega variáveis do .env automaticamente
load_dotenv()

# Modelos
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Caminhos
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./data/faiss_index.pkl")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

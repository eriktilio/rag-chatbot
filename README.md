# RAG CHATBOT API

Uma **API simples e modular** de **RAG (Retrieval-Augmented Generation)** construída com **FastAPI**, **LangChain**, **FAISS** e **Hugging Face Embeddings**, usando o modelo **Gemini Flash** (Google Vertex AI) como LLM.

## Estrutura do Projeto

```bash
├── 📁 data
├── 📁 src
│   ├── 📁 api
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 routes.py
│   ├── 📁 core
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 embeddings.py
│   │   ├── 🐍 rag.py
│   │   └── 🐍 vectorstorage.py
│   ├── 🐍 __init__.py
│   ├── 🐍 config.py
│   └── 🐍 main.py
├── ⚙️ .env.sample
├── ⚙️ .gitignore
├── 📝 README.md
├── 📄 poetry.lock
└── ⚙️ pyproject.toml
```

## Configuração do Ambiente

```bash
poetry install
```

## Rodar o servidor

### Executar

```bash
poetry run uvicorn src.main:app --reload
```

### Swagger

```http
http://127.0.0.1:8000/docs
```

## Endpoints

| Método   | Endpoint              | Descrição                            | Tipo de Corpo          |
|-----------|------------------------|--------------------------------------|------------------------|
| `POST`    | `/upload`              | Envia um arquivo PDF para indexação  | `multipart/form-data`  |
| `POST`    | `/query`               | Faz uma pergunta ao modelo RAG       | `application/json`     |
| `GET`     | `/files`               | Lista todos os PDFs carregados       | `N/A`                  |
| `DELETE`  | `/files/{filename}`    | Remove um PDF do índice vetorial     | `N/A`                  |

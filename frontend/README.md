# RAG CHATBOT APP

Este projeto contém o frontend do chatbot RAG usando **Streamlit**, gerenciado com **Poetry** e preparado para rodar em **Docker**.

---

## Estrutura do Projeto

```
├── 📁 src
│   ├── 🐍 app.py
│   └── 🐍 service.py
├── ⚙️ .gitignore
├── 🐳 Dockerfile
├── 📝 README.md
├── ⚙️ docker-compose.yml
├── 📄 poetry.lock
└── ⚙️ pyproject.toml
```

## 🚀 Como rodar o projeto localmente (sem Docker)

### 1. Instalar dependências

```bash
poetry install
```

### 2. Rodar o app

```bash
poetry run streamlit run app.py
```

O app estará disponível em: 👉 <http://localhost:8501>

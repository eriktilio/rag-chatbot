# Usa imagem leve do Python
FROM python:3.13-slim

# Instala dependências básicas
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instala o Poetry globalmente
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de configuração primeiro (para aproveitar cache)
COPY pyproject.toml poetry.lock* ./

# Instala dependências
RUN poetry install --no-root --no-interaction --no-ansi

# Copia o código da aplicação
COPY . .

EXPOSE 8000

# Comando final (exemplo para FastAPI)
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

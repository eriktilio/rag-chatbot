FROM python:3.13-slim

# Instala dependências básicas
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instala o Poetry globalmente
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

# Definir diretório de trabalho
WORKDIR /app

# Copiar configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry para não criar ambiente virtual
RUN poetry config virtualenvs.create false

# Instalar dependências (sem código ainda → mais cache!)
RUN poetry install --no-interaction --no-ansi

# Copia o código da aplicação
COPY . .

# Expor porta do Streamlit
EXPOSE 8501

# Comando de entrada
CMD ["poetry", "run", "streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]

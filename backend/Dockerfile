# Usa imagem leve do Python
FROM python:3.13-slim

# 1. Instala o 'uv' copiando da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Instala dependências básicas do sistema
#RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# 3. Configurações de ambiente
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Define o local do ambiente virtual e adiciona ao PATH
# Isso elimina a necessidade de prefixos como "poetry run" ou "uv run"
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Define o diretório de trabalho
WORKDIR /app

# 4. Copia arquivos de configuração
# Renomeia o pyproject_uv.toml para o padrão esperado pelo uv
COPY pyproject_uv.toml pyproject.toml
COPY uv.lock* ./

# 5. Instala dependências
# --no-install-project: Instala apenas as bibliotecas, ignorando o código do projeto por enquanto
# Sem --frozen pois você ainda não tem o uv.lock gerado
RUN uv sync --no-dev --no-install-project --no-cache

# 6. Copia o código da aplicação
COPY . .

# Expose a porta do FastAPI
EXPOSE 8000

# 7. Comando final
# Como o ambiente virtual já está no PATH, chamamos 'uvicorn' diretamente
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
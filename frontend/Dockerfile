FROM python:3.13-slim

# 1. Instala o 'uv' copiando da imagem oficial (método mais rápido e seguro)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Instala dependências de sistema necessárias
#RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# 3. Configurações de ambiente
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Define o local do ambiente virtual e adiciona ao PATH
# Isso substitui a necessidade de "virtualenvs.create false" do Poetry,
# pois torna o venv transparente para o sistema.
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# 4. Copia os arquivos de definição de dependências
# O uv espera por padrão o arquivo pyproject.toml, então renomeamos o seu arquivo específico
COPY pyproject_uv.toml pyproject.toml
COPY uv.lock* ./

# 5. Instala as dependências
# Removemos --frozen para permitir que o uv resolva as dependências na hora
# --no-dev: Não instala dependências de desenvolvimento
# --no-install-project: Instala apenas as libs, não o seu código (melhora o cache do Docker)
RUN uv sync --no-dev --no-install-project --no-cache

# 6. Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8501

# 7. Comando de entrada
# Como o VIRTUAL_ENV está no PATH, podemos chamar 'streamlit' diretamente
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
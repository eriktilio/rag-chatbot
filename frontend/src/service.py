import requests


class RAGService:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    # -------------------------------
    # LISTAR ARQUIVOS
    # -------------------------------
    def get_indexed_files(self):
        """Busca a lista de arquivos PDF indexados."""
        try:
            response = requests.get(f"{self.api_url}/files")
            response.raise_for_status()
            return response.json().get("uploaded_pdfs", [])
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # -------------------------------
    # UPLOAD DE PDF
    # -------------------------------
    def upload_file(self, file):
        """Envia um arquivo PDF para a API para ser indexado."""
        files = {"file": (file.name, file.getvalue(), file.type)}
        try:
            response = requests.post(f"{self.api_url}/upload", files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # -------------------------------
    # REMOVER PDF
    # -------------------------------
    def delete_file(self, filename):
        """Solicita a remoção de um arquivo do índice."""
        try:
            response = requests.delete(f"{self.api_url}/files/{filename}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # -------------------------------
    # CONSULTAR RAG
    # -------------------------------
    def query_rag(self, question: str):
        """Envia uma pergunta para o modelo RAG."""
        try:
            response = requests.post(
                f"{self.api_url}/query",
                json={"question": question}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


# Instância padrão para uso no Streamlit
rag_service = RAGService(api_url="http://backend:8000")

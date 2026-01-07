import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"

def get_embedding(text: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["embedding"]

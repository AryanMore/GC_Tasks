import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_document():
    payload = {
        "id": 401,
        "text": "Vector databases enable semantic similarity search."
    }
    r = client.post("/documents", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "inserted"


def test_batch_create_documents():
    payload = {
        "documents": [
            {"id": 402, "text": "FastAPI builds production ready APIs."},
            {"id": 403, "text": "Qdrant stores vector embeddings efficiently."}
        ]
    }
    r = client.post("/documents/batch", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "batch_inserted"


def test_search_documents():
    r = client.get("/documents/search?query=semantic vector database")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_update_document():
    payload = {
        "id": 401,
        "text": "Vector databases efficiently manage embeddings for AI systems."
    }
    r = client.put("/documents/401", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "updated"


def test_delete_document():
    r = client.delete("/documents/401")
    assert r.status_code == 200
    assert r.json()["status"] == "deleted"

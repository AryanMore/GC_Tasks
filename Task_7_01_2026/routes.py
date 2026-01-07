from fastapi import APIRouter
from qdrant_client.http.models import PointStruct
from schemas import Document
from embeddings import get_embedding
from qdrant_connect import client, COLLECTION_NAME

router = APIRouter()

# ---------------- CREATE ----------------
@router.post("/documents")
def add_document(doc: Document):
    vector = get_embedding(doc.text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=doc.id,
                vector=vector,
                payload={"text": doc.text}
            )
        ]
    )
    return {"status": "inserted", "id": doc.id}


# ---------------- READ (Vector Search) ----------------
@router.get("/documents/search")
def search_documents(query: str, limit: int = 5):
    query_vector = get_embedding(query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )

    return results


# ---------------- UPDATE ----------------
@router.put("/documents/{doc_id}")
def update_document(doc_id: int, doc: Document):
    vector = get_embedding(doc.text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=doc_id,
                vector=vector,
                payload={"text": doc.text}
            )
        ]
    )
    return {"status": "updated", "id": doc_id}


# ---------------- DELETE ----------------
@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[doc_id]
    )
    return {"status": "deleted", "id": doc_id}

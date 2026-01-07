from embeddings import get_embedding
from qdrant_connect import client, COLLECTION_NAME
from schemas import Document
from qdrant_client.http.models import PointStruct
from schemas import DocumentBatch
from qdrant_client.http.models import PointStruct
# ---------------- CREATE ----------------
def create(doc: Document):
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

def create_many(batch: DocumentBatch):
    points = []

    for doc in batch.documents:
        vector = get_embedding(doc.text)
        points.append(
            PointStruct(
                id=doc.id,
                vector=vector,
                payload={"text": doc.text}
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return {"status": "batch_inserted", "count": len(points)}


# ---------------- READ ----------------
def search(query: str, limit: int = 5):
    query_vector = get_embedding(query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        with_vectors=True
    )
    return results


# ---------------- UPDATE ----------------
def update(doc_id: int, doc: Document):
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
def delete_document(doc_id: int):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[doc_id]
    )
    return {"status": "deleted", "id": doc_id}

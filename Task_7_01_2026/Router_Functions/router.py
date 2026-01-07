from fastapi import APIRouter
from schemas import Document
from Router_Functions.router_functions import create, search, update, delete_document
from schemas import DocumentBatch
from qdrant_client.http.models import PointStruct
from Router_Functions.router_functions import create_many

router = APIRouter()

# ---------------- CREATE ----------------
@router.post("/documents")
def add_document(doc: Document):
    return create(doc)

@router.post("/documents/batch")
def add_documents(batch: DocumentBatch):
    return create_many(batch)

# ---------------- READ ----------------
@router.get("/documents/search")
def search_documents(query: str, limit: int = 5):
    return search(query, limit)

# ---------------- UPDATE ----------------
@router.put("/documents/{doc_id}")
def update_document(doc_id: int, doc: Document):
    return update(doc_id, doc)

# ---------------- DELETE ----------------
@router.delete("/documents/{doc_id}")
def delete_doc(doc_id: int):
    return delete_document(doc_id)

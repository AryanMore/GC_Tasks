from loaders.md_loader import load_md_files
from embeddings import get_embedding
from qdrant_db import client, COLLECTION
from qdrant_client.http.models import PointStruct
import uuid


docs = load_md_files("data/qdrant_docs")

points = []
for d in docs:
    points.append(PointStruct(
        id=str(uuid.uuid4()),
        vector=get_embedding(d["content"]),
        payload=d
    ))

client.upsert(collection_name=COLLECTION, points=points)
print("Markdown docs ingested.")

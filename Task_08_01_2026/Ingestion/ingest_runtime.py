from loaders.md_loader import parse_markdown
from embeddings import get_embedding
from qdrant_db import client, COLLECTION
from qdrant_client.http.models import PointStruct
import uuid

def insert_markdown_docs(docs):
    points = []

    for doc in docs:
        blocks = parse_markdown(doc["content"])

        for pos, b in enumerate(blocks):
            if len(b["content"].split()) < 20:
                continue

            vec = get_embedding(b["content"])

            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload={
                    "doc": doc["filename"],
                    "heading": b["heading"],
                    "type": b["type"],
                    "language": b["language"],
                    "content": b["content"],
                    "position": pos
                }
            ))

    if points:
        client.upsert(collection_name=COLLECTION, points=points)

    return len(points)

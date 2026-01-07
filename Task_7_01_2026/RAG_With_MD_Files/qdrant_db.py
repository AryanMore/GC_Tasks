from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL or QDRANT_API_KEY not set")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)

COLLECTION = "qdrant_md_docs"

collections = client.get_collections().collections
existing = [c.name for c in collections]

if COLLECTION not in existing:
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )


client.create_payload_index(
    collection_name=COLLECTION,
    field_name="content",
    field_schema=PayloadSchemaType.TEXT
)

client.create_payload_index(COLLECTION, "type", PayloadSchemaType.KEYWORD)
client.create_payload_index(COLLECTION, "language", PayloadSchemaType.KEYWORD)
client.create_payload_index(COLLECTION, "heading", PayloadSchemaType.TEXT)


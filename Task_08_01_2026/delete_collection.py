from qdrant_db import client, COLLECTION
from qdrant_client.http.models import Filter, FilterSelector

def delete_all():
    client.delete(
        collection_name=COLLECTION,
        points_selector=FilterSelector(filter=Filter())
    )

from qdrant_db import client, COLLECTION
import json
from pathlib import Path

Path("DB_Dump").mkdir(exist_ok=True)

scroll = None
all_points = []

while True:
    points, scroll = client.scroll(
        collection_name=COLLECTION,
        limit=100,
        with_vectors=True,
        with_payload=True,
        offset=scroll
    )

    all_points.extend(points)

    if scroll is None:
        break

dump_file = Path("DB_Dump/dump.json")
dump_file.write_text(json.dumps([p.dict() for p in all_points], indent=2))

print(f"Dumped {len(all_points)} points into DB_Dump/dump.json")

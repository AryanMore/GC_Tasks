import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_Name")]

collection = db["products"]

collection.create_index(
    [
        ("brand", ASCENDING),
        ("name", ASCENDING),
        ("quantity.value", ASCENDING),
        ("quantity.unit", ASCENDING)
    ],
    unique = True
)





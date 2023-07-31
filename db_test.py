from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
db = MongoClient(os.getenv("MONGODB_URI")).mongo_notes

def get_all_notes():
    docs = db.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "file": doc["file"],
        })
    return new_docs

print(get_all_notes())
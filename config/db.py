import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
conn = MongoClient(MONGO_URI)
db = conn.mongo_notes
if __name__ == "__main__":
    print(conn.server_info())
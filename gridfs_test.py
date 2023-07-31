from pymongo import MongoClient
import os
from dotenv import load_dotenv
import gridfs
import base64
load_dotenv()
conn = MongoClient(os.getenv("MONGODB_URI"))
fs = gridfs.GridFS(conn.mongo_notes, collection="files")
print(conn.server_info())
# docs = conn.mongo_notes.notes.find({})
# for doc in docs:
#     print(doc)
file: str = "static/test.jpg"

# uploading file
with open(file, "rb") as f:
    data = f.read()
    # print(data)
    fs.put(data, filename="test.jpg")
    print("file uploaded")

# downloading file
data = conn.mongo_notes.files.files.find_one({"filename": "test.html"})
# print(data)
file_id = data["_id"]
# # print(file_id)
file = fs.get(file_id).read()
with open("static/downloaded.jpg", "wb") as f:
    f.write(file)
    encoded_data = base64.b64encode(file)
    print("file downloaded")
print(encoded_data.decode("utf-8"))
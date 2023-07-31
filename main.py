from fastapi import FastAPI, Request, File, UploadFile, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.db import db
from models.note import Note
from schemas.note import noteEntity, notesEntity
from typing import Annotated, Union, Optional
import gridfs
# from deta import Deta
from bson import ObjectId

app = FastAPI()
fs = gridfs.GridFS(db, collection="files")

# deta = Deta("d098QJarhFU7_AzQwFXjrzwM4XyPPWUaoJMQ9udFrbVaf")
# drive = deta.Drive("notes")

# serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# serving templates statically
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")
# creating templates
templates: Jinja2Templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/new")
async def new(
        title: Annotated[str, Form()],
        desc: Annotated[str, Form()],
        # important: Annotated[bool | None = None, Form()],
        noteFile: Annotated[Optional[UploadFile], File()],
):
    if noteFile is not None:
        file_name = noteFile.filename
        file_type = noteFile.content_type
        data = await noteFile.read()
        fs.put(data, filename=file_name)
        print("file uploaded")
        # save file to static folder
        # with open(f"static/{noteFile.filename}", "wb") as f:
        #     f.write(data)
        # save file to deta drive
        # deta_file = drive.put(file_name, data=data)
    else:
        file_name = None
        file_type = None
    new_note = {
        "title": title,
        "desc": desc,
        # "important": important,
        "file": file_name,
        "file_type": file_type
    }
    inserted_note = Note(**new_note)
    print(inserted_note)
    inserted_note = db.notes.insert_one(dict(inserted_note))
    # uploading file to mongodb
    # if noteFile is not None:
    #     data = noteFile.read()
    #     fs.put(data, filename=noteFile.filename)
    #     print("file uploaded")
    #     with open(f"static{noteFile.filename}", "wb") as f:
    #         f.write(data)
    return {"message": "note created successfully", "note": new_note}

@app.get("/view", response_class=HTMLResponse)
async def view(request: Request):
    docs = db.notes.find({})
    # print(docs)
    new_docs = []
    for doc in docs:
        # print(doc)
        new_docs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "file": doc["file"],
        })
    # print(new_docs)
    return templates.TemplateResponse("view.html", {"request": request, "newDocs": new_docs})

@app.get("/delete/{id}")
async def delete(id: str):
    db.notes.delete_one({"_id": ObjectId(id)})
    return {"message": "note deleted successfully"}

@app.get("/download/{id}")
async def download(id: str):
    note = db.notes.find_one({"_id": ObjectId(id)})
    file_name = note["file"]
    file_type = note["file_type"]
    if file_name is not None:
        data = fs.get_last_version(filename=file_name).read()
        return Response(content=data, media_type=file_type)   
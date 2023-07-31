from fastapi import APIRouter, Request, File, UploadFile, Form
from config.db import db
from models.note import Note
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from typing import Annotated, Union, Optional
import gridfs
from bson import ObjectId

note = APIRouter()

templates: Jinja2Templates = Jinja2Templates(directory="templates")

fs = gridfs.GridFS(db, collection="files")

@note.post("/new")
async def new(
        title: Annotated[str, Form()],
        desc: Annotated[str, Form()],
        # important: Annotated[bool | None = None, Form()],
        noteFile: Annotated[Optional[UploadFile], File()],
):
    if noteFile is not None:
        file_name = noteFile.filename
        data = await noteFile.read()
        fs.put(data, filename=noteFile.filename)
        print("file uploaded")
        # save file to static folder
        with open(f"static/{noteFile.filename}", "wb") as f:
            f.write(data)

    else:
        file_name = None
    new_note = {
        "title": title,
        "desc": desc,
        # "important": important,
        "file": file_name,
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

@note.get("/view", response_class=HTMLResponse)
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

@note.get("/delete/{id}")
async def delete(id: str):
    db.notes.delete_one({"_id": ObjectId(id)})
    return {"message": "note deleted successfully"}

# normal form data
# @note.post("/new")
# async def new(request: Request):
#     form = await request.form()
#     formDict = dict(form)
#     print(formDict)
#     note = db.notes.insert_one(formDict)
#     return {"message": "note created successfully", "note": formDict}


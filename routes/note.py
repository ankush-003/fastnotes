from fastapi import APIRouter, Request, File, UploadFile, Form, Response
from config.db import db
from models.note import Note
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from typing import Annotated, Union, Optional
import gridfs
from bson import ObjectId

note = APIRouter()

templates: Jinja2Templates = Jinja2Templates(directory="templates")

fs = gridfs.GridFS(db, collection="files")

@note.post("/new", response_class=HTMLResponse)
async def new(
        request: Request,
        title: Annotated[str, Form()],
        desc: Annotated[str, Form()],
        # important: Annotated[bool | None = None, Form()],
        noteFile: Annotated[Optional[UploadFile], File()],
):
    if noteFile is not None:
        file_name = noteFile.filename
        file_type = noteFile.content_type
        data = await noteFile.read()
        fs.put(data, filename=noteFile.filename)
        print("file uploaded")
        # save file to static folder
        # with open(f"static/{noteFile.filename}", "wb") as f:
        #     f.write(data)

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
    # return {"message": "note created successfully", "note": new_note}
    return templates.TemplateResponse("upload.html", {"request": request, "message": "note created successfully"})

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

@note.get("/delete/{id}", response_class=RedirectResponse)
async def delete(id: str):
    note = db.notes.find_one({"_id": ObjectId(id)})
    file_name = note["file"]
    fs.delete(fs.find_one({"filename": file_name})._id)
    db.notes.delete_one({"_id": ObjectId(id)})
    # return {"message": "note deleted successfully"}
    return RedirectResponse(url="/view")

@note.get("/download/{id}")
async def download(id: str):
    note = db.notes.find_one({"_id": ObjectId(id)})
    file_name = note["file"]
    file_type = note["file_type"]
    data = fs.get_last_version(filename=file_name).read()
    return Response(content=data, media_type=file_type)

# normal form data
# @note.post("/new")
# async def new(request: Request):
#     form = await request.form()
#     formDict = dict(form)
#     print(formDict)
#     note = db.notes.insert_one(formDict)
#     return {"message": "note created successfully", "note": formDict}



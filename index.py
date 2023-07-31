from fastapi import FastAPI, Request
from routes.note import note
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI()

# serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# serving templates statically
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")
# creating templates
templates: Jinja2Templates = Jinja2Templates(directory="templates")

app.include_router(note)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
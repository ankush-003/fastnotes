from pydantic import BaseModel


class Note(BaseModel):
    title: str
    desc: str
    # important: bool | None = None
    file: str | None = None

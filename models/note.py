from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    title: str
    desc: str
    # important: bool | None = None
    file: Optional[str] = None

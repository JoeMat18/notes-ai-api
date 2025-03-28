from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    summary: Optional[str] = None

    class Config:
        orm_mode = True # Allows to work with SQLAlchemy objects
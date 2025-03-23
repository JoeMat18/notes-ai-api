from sqlalchemy.orm import Session
from app import models, schemas

def create_note(db: Session, note: schemas.NoteCreate):
    """
    Create a new note
    """
    db_note = models.Note(
        title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(db: Session, skip: int = 0, limit = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()
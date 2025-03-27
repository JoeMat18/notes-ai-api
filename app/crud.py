from sqlalchemy.orm import Session
from app import models, schemas

def create_note(db: Session, note: schemas.NoteCreate):
    """
    ???
    """
    db_note = models.Note(
        title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(db: Session, skip: int = 0, limit = 100):
    """
    ???
    """
    return db.query(models.Note).offset(skip).limit(limit).all()

def get_note_by_id(db: Session, note_id: int):
    """
    ???
    """
    return db.query(models.Note).filter(models.Note.id == note_id)

def delete_note(db: Session, note_id: int):
    """
    ???
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note

def update_note(db: Session, note_id: int, note_data: schemas.NoteCreate):
    """
    ???
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        note.title = note_data.title
        note.content = note_data.content
        db.commit()
        db.refresh(note)
    return note

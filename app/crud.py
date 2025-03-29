from sqlalchemy.orm import Session
from app import models, schemas

def create_note(db: Session, note: schemas.NoteCreate):
    """
    Create a new note in the database.
    """
    db_note = models.Note(
        title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(db: Session, skip: int = 0, limit = 100):
    """
    Retrieve a list of all notes with pagination.
    """
    return db.query(models.Note).offset(skip).limit(limit).all()

def get_note_by_id(db: Session, note_id: int):
    """
    Retrieve a single note by its ID.
    """
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def delete_note(db: Session, note_id: int):
    """
    Delete a note by its ID.
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note

def delete_all_notes(db: Session):
    """
    Delete all notes from the database.
    """
    db.query(models.Note).delete()
    db.commit()

def update_note(db: Session, note_id: int, note_update: schemas.NoteUpdate):
    """
    Update a note's title and/or content by its ID.
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        if note_update.title is not None and note_update.title != "string":
            note.title = note_update.title
        if note_update.content is not None and note_update.content != "string":
            note.content = note_update.content
        db.commit()
        db.refresh(note)
    return note

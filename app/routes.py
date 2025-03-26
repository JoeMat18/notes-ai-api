from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from app import ai, models
from fastapi import HTTPException

notes_router = APIRouter(prefix="/notes", tags=['notes'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@notes_router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)

@notes_router.get("/", response_model=list[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_notes(db=db, skip=skip, limit=limit)

@notes_router.post("{note_id}/summarize")
def summarize_note(note_id: int, db:  Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = ai.summarize_text(note.content)

    return {
        "note_id": note.id,
        "original": note.content,
        "summary": summary
    }


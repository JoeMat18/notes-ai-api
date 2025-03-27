from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from app import ai, models

notes_router = APIRouter(prefix="/notes", tags=['notes'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@notes_router.post("/", response_model=schemas.Note, summary="Create a note")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note with title and content.
    """
    return crud.create_note(db=db, note=note)

@notes_router.get("/", response_model=list[schemas.Note], summary="List all notes")
def read_notes(
        skip: int = Query(0, description="How many notes to skip"),
        limit: int = Query(100, description="Maximum number of notes to return"),
        db: Session = Depends(get_db)
):
    """
    Get a list of all notes with pagination.
    """
    return crud.get_all_notes(db=db, skip=skip, limit=limit)


@notes_router.get("/{note_id}", response_model=schemas.Note, summary="Get a note by ID")
def read_note(
        note_id: int = Path(..., description="ID of the note"),
        db: Session = Depends(get_db)
):
    """
    Get a single note by its ID.
    """
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@notes_router.put("/{note_id}", response_model=schemas.Note, summary="Update a note")
def update_note(
    note_id: int = Path(..., description="ID of the note to update"),
    note: schemas.NoteCreate = ...,
    db: Session = Depends(get_db)
):
    """
    Update a note's title and content by ID.
    """
    note = crud.update_note(db, note_id, note)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@notes_router.delete("/{note_id}", response_model=schemas.Note, summary="Delete a note")
def delete_note(
    note_id: int = Path(..., description="ID of the note to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a note by ID.
    """
    note = crud.delete_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": f"Note '{note_id}' deleted"}



@notes_router.post("/{note_id}/summarize", summary="Summarize a note by ID")
def summarize_note(
    note_id: int = Path(..., description="ID of the note to summarize"),
    db: Session = Depends(get_db)
):
    """
    Summarize the content of a note using AI.
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = ai.summarize_text(note.content)

    return {
        "note_id": note.id,
        "original": note.content,
        "summary": summary
    }
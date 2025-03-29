from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models, ai
from app.routes import notes_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(notes_router)

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_notes(request: Request):
    db = SessionLocal()
    notes = db.query(models.Note).all()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.post("/create")
def create_note(title: str = Form(...), content: str = Form(...)):
    db = SessionLocal()
    note = models.Note(title=title, content=content)
    db.add(note)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/summarize/{note_id}")
def summarize_note(note_id: int):
    db = SessionLocal()
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        summary = ai.summarize_text(note.content)
        note.summary = summary
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{note_id}")
def delete_note(note_id: int):
    db = SessionLocal()
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/delete_all")
def delete_all_notes():
    db = SessionLocal()
    db.query(models.Note).delete()
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/update/{note_id}")
def update_note(note_id: int, title: str = Form(...), content: str = Form(...)):
    db = SessionLocal()
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        note.title = title
        note.content = content
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/search")
def search_notes(query: str, request: Request):
    db = SessionLocal()
    results = db.query(models.Note).filter(
        models.Note.title.ilike(f"%{query}%") |
        models.Note.content.ilike(f"%{query}%")
    ).all()
    return templates.TemplateResponse("index.html", {"request": request, "notes": results})

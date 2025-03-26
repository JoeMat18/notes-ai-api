from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models, ai

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
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

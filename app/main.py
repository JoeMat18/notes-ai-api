from app.database import Base, engine
from app.routes import notes_router
from fastapi import FastAPI


Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Notes API with AI Summarizer")

app.include_router(notes_router)

## 📝 Notes AI API

**Notes AI API** is a RESTful microservice that allows you to create, read, update, delete, and summarize notes using an AI-powered model.

### 📌 Features

- ✅ Full CRUD functionality for notes
- ✨ Text summarization using a transformer-based AI model
- 🧠 Integrates with Hugging Face transformers
- 💾 PostgreSQL database support
- 🐳 Dockerized for easy deployment
- 📘 Auto-generated interactive API docs at `/docs`

---

### 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/JoeMat18/notes-ai-api
cd notes-ai-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost/notes_db
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

---

### 🧠 AI Summarization

Summarization is handled using the Hugging Face model `sshleifer/distilbart-cnn-12-6`.

Example endpoint:
```http
POST /notes/{note_id}/summarize
```

---

### 📁 Project Structure

```
app/
├── ai.py               # AI summarization logic
├── crud.py             # Database operations
├── database.py         # PostgreSQL configuration
├── models.py           # SQLAlchemy models
├── routes.py           # API endpoints (FastAPI routers)
├── schemas.py          # Pydantic schemas
├── templates/          # HTML templates
└── main.py             # Entry point of the app
```
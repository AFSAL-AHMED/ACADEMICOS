from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

import notion_service

app = FastAPI(title="ACADEMICOS Journal API")

# Allow Expo app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request Models ────────────────────────────────────────────────────────────

class JournalEntry(BaseModel):
    title: str
    entry: str
    topics: List[str] = []
    difficulty: int = 3  # 1-5
    date: Optional[str] = None  # ISO format: "2026-05-03"

# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ACADEMICOS Journal API is running 🎓"}


@app.post("/journal/entry")
def create_entry(data: JournalEntry):
    try:
        entry_date = data.date or str(date.today())
        result = notion_service.save_entry(
            title=data.title,
            entry_text=data.entry,
            topics=data.topics,
            difficulty=data.difficulty,
            entry_date=entry_date,
        )
        return {"success": True, "notion_page": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/journal/entries")
def list_entries():
    try:
        entries = notion_service.get_entries()
        return {"entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/journal/streak")
def get_streak():
    try:
        return notion_service.get_streak()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

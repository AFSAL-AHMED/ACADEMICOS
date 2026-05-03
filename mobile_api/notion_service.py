import os
from datetime import datetime, date
from typing import Optional, List
from notion_client import Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

notion = Client(auth=os.getenv("NOTION_API_KEY"))
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID")

JOURNAL_DB_NAME = "Daily Learning Journal"

# ── Helpers ─────────────────────────────────────────────────────────────────

def _get_or_create_journal_db() -> str:
    """Returns the journal database ID, creating it if it doesn't exist."""
    # Search for existing database
    results = notion.search(
        query=JOURNAL_DB_NAME,
        filter={"value": "database", "property": "object"}
    ).get("results", [])

    for db in results:
        if db.get("title", [{}])[0].get("plain_text", "") == JOURNAL_DB_NAME:
            return db["id"]

    # Create the database
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        title=[{"type": "text", "text": {"content": JOURNAL_DB_NAME}}],
        properties={
            "Title": {"title": {}},
            "Date": {"date": {}},
            "Topics": {"multi_select": {}},
            "Difficulty": {"select": {
                "options": [
                    {"name": "⭐ Easy",       "color": "green"},
                    {"name": "⭐⭐ Medium",    "color": "yellow"},
                    {"name": "⭐⭐⭐ Hard",    "color": "orange"},
                    {"name": "⭐⭐⭐⭐ Tough", "color": "red"},
                    {"name": "⭐⭐⭐⭐⭐ Extreme", "color": "purple"},
                ]
            }},
            "Entry": {"rich_text": {}},
        }
    )
    return db["id"]


DIFFICULTY_MAP = {
    1: "⭐ Easy",
    2: "⭐⭐ Medium",
    3: "⭐⭐⭐ Hard",
    4: "⭐⭐⭐⭐ Tough",
    5: "⭐⭐⭐⭐⭐ Extreme",
}

# ── Public Functions ─────────────────────────────────────────────────────────

def save_entry(title: str, entry_text: str, topics: List[str], difficulty: int, entry_date: str) -> dict:
    """Save a journal entry to the Notion database."""
    db_id = _get_or_create_journal_db()

    difficulty_label = DIFFICULTY_MAP.get(difficulty, "⭐⭐⭐ Hard")

    page = notion.pages.create(
        parent={"database_id": db_id},
        properties={
            "Title":      {"title": [{"text": {"content": title}}]},
            "Date":       {"date": {"start": entry_date}},
            "Topics":     {"multi_select": [{"name": t} for t in topics]},
            "Difficulty": {"select": {"name": difficulty_label}},
            "Entry":      {"rich_text": [{"text": {"content": entry_text}}]},
        }
    )
    return {"id": page["id"], "url": page["url"]}


def get_entries() -> List[dict]:
    """Fetch all journal entries from Notion, sorted by date descending."""
    db_id = _get_or_create_journal_db()

    response = notion.databases.query(
        database_id=db_id,
        sorts=[{"property": "Date", "direction": "descending"}]
    )

    entries = []
    for page in response.get("results", []):
        props = page["properties"]

        title = ""
        if props.get("Title", {}).get("title"):
            title = props["Title"]["title"][0]["plain_text"]

        entry_text = ""
        if props.get("Entry", {}).get("rich_text"):
            entry_text = props["Entry"]["rich_text"][0]["plain_text"]

        entry_date = None
        if props.get("Date", {}).get("date"):
            entry_date = props["Date"]["date"]["start"]

        topics = [t["name"] for t in props.get("Topics", {}).get("multi_select", [])]

        difficulty = props.get("Difficulty", {}).get("select")
        difficulty_name = difficulty["name"] if difficulty else ""

        entries.append({
            "id":         page["id"],
            "title":      title,
            "entry":      entry_text,
            "date":       entry_date,
            "topics":     topics,
            "difficulty": difficulty_name,
        })

    return entries


def get_streak() -> dict:
    """Calculate the current study streak (consecutive days with entries)."""
    entries = get_entries()
    if not entries:
        return {"streak": 0, "total_entries": 0}

    # Collect unique dates
    dates = sorted(
        set(e["date"] for e in entries if e["date"]),
        reverse=True
    )

    streak = 0
    today = date.today()

    for i, d in enumerate(dates):
        entry_date = date.fromisoformat(d)
        expected = today - __import__('datetime').timedelta(days=i)
        if entry_date == expected:
            streak += 1
        else:
            break

    return {"streak": streak, "total_entries": len(entries)}

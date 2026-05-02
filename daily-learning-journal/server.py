"""
Daily Learning Journal — Notion Logger
Pure Python. No AI. Just you and your progress.
"""

import os
from datetime import date
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion      = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("DATABASE_ID")
DS_ID       = "3540cab0-0e4d-80f4-aff4-000b79dce777"


# ─── helpers ──────────────────────────────────────────────────────────────────
def _get_text(props, key):
    rt = props.get(key, {}).get("rich_text", [])
    return rt[0]["plain_text"] if rt else "—"

def _get_select(props, key):
    sel = props.get(key, {}).get("select")
    return sel["name"] if sel else "—"

def _get_title(props, key="Day"):
    t = props.get(key, {}).get("title", [])
    return t[0]["plain_text"] if t else "—"

def _get_number(props, key):
    return props.get(key, {}).get("number") or 0

def _get_date(props):
    d = props.get("Date", {}).get("date")
    return d["start"] if d else "—"


# ─── FUNCTION 1: Add a daily log ──────────────────────────────────────────────
def add_learning_log(
    day_title,
    topic,
    hours_spent,
    mood,
    key_takeaways,
    resources_used="",
    tomorrows_goal="",
    streak_day=1,
    log_date="",
):
    if not log_date:
        log_date = date.today().isoformat()

    page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Day":             {"title": [{"text": {"content": day_title}}]},
            "Date":            {"date": {"start": log_date}},
            "Topic":           {"select": {"name": topic}},
            "Hours Spent":     {"number": hours_spent},
            "Mood":            {"select": {"name": mood}},
            "Key Takeaways":   {"rich_text": [{"text": {"content": key_takeaways}}]},
            "Resources Used":  {"rich_text": [{"text": {"content": resources_used}}]},
            "Tomorrow's Goal": {"rich_text": [{"text": {"content": tomorrows_goal}}]},
            "Streak Day":      {"number": streak_day},
        },
    )
    return f"Log added!\nDate: {log_date} | Topic: {topic} | {hours_spent}h | {mood}\n{page.get('url','')}"


# ─── FUNCTION 2: Get today's log ──────────────────────────────────────────────
def get_todays_log():
    today = date.today().isoformat()
    res   = notion.request(
        path=f"data_sources/{DS_ID}/query",
        method="POST",
        body={"filter": {"property": "Date", "date": {"equals": today}}},
    )
    pages = res.get("results", [])
    if not pages:
        return f"No log for today ({today}). Time to log your learning!"

    p      = pages[0]["properties"]
    tmr    = "Tomorrow's Goal"
    return (
        f"\nToday's Log — {today}\n"
        f"{'─'*40}\n"
        f"Day        : {_get_title(p)}\n"
        f"Topic      : {_get_select(p, 'Topic')}\n"
        f"Hours      : {_get_number(p, 'Hours Spent')}h\n"
        f"Mood       : {_get_select(p, 'Mood')}\n"
        f"Streak Day : #{_get_number(p, 'Streak Day')}\n\n"
        f"Key Takeaways:\n  {_get_text(p, 'Key Takeaways')}\n\n"
        f"Resources Used:\n  {_get_text(p, 'Resources Used')}\n\n"
        f"Tomorrow's Goal:\n  {_get_text(p, tmr)}\n"
    )


# ─── FUNCTION 3: List recent logs ─────────────────────────────────────────────
def list_recent_logs(limit=7):
    res = notion.request(
        path=f"data_sources/{DS_ID}/query",
        method="POST",
        body={
            "sorts": [{"property": "Date", "direction": "descending"}],
            "page_size": limit,
        },
    )
    pages = res.get("results", [])
    if not pages:
        return "No logs yet. Start logging today!"

    lines = [f"\nLast {len(pages)} Log(s):\n{'─'*40}"]
    for page in pages:
        p = page["properties"]
        lines.append(
            f"{_get_date(p)} | Day #{_get_number(p,'Streak Day')} | "
            f"{_get_select(p,'Topic')} | {_get_number(p,'Hours Spent')}h | {_get_select(p,'Mood')}\n"
            f"  -> {_get_title(p)}"
        )
    return "\n\n".join(lines)


# ─── FUNCTION 4: Stats ────────────────────────────────────────────────────────
def get_stats():
    res   = notion.request(
        path=f"data_sources/{DS_ID}/query",
        method="POST",
        body={"sorts": [{"property": "Date", "direction": "descending"}]},
    )
    pages = res.get("results", [])
    if not pages:
        return "No logs yet. Start your journey today!"

    total_hours, topic_counts, mood_counts, max_streak = 0, {}, {}, 0

    for page in pages:
        p = page["properties"]
        total_hours += _get_number(p, "Hours Spent")
        t = _get_select(p, "Topic");  topic_counts[t] = topic_counts.get(t, 0) + 1
        m = _get_select(p, "Mood");   mood_counts[m]  = mood_counts.get(m, 0) + 1
        s = _get_number(p, "Streak Day")
        if s > max_streak:
            max_streak = s

    top_topic  = max(topic_counts, key=topic_counts.get) if topic_counts else "—"
    topics_str = "\n".join(f"  {t}: {c} day(s)" for t, c in sorted(topic_counts.items(), key=lambda x: -x[1]))

    return (
        f"\nLearning Journal Stats\n{'─'*40}\n"
        f"Total Days Logged : {len(pages)}\n"
        f"Total Hours       : {total_hours:.1f}h\n"
        f"Best Streak       : Day #{max_streak}\n"
        f"Favourite Topic   : {top_topic}\n\n"
        f"Topics Breakdown:\n{topics_str}\n"
    )


# ─── FUNCTION 5: Search by topic ──────────────────────────────────────────────
def search_logs_by_topic(topic):
    res = notion.request(
        path=f"data_sources/{DS_ID}/query",
        method="POST",
        body={
            "filter": {"property": "Topic", "select": {"equals": topic}},
            "sorts":  [{"property": "Date", "direction": "descending"}],
        },
    )
    pages = res.get("results", [])
    if not pages:
        return f"No logs found for topic: '{topic}'"

    lines = [f"\nLogs for '{topic}' ({len(pages)} entries):\n{'─'*40}"]
    for page in pages:
        p  = page["properties"]
        tk = _get_text(p, "Key Takeaways")
        tk = tk[:80] + "..." if len(tk) > 80 else tk
        lines.append(f"{_get_date(p)} | {_get_number(p,'Hours Spent')}h\n  {_get_title(p)}\n  {tk}")
    return "\n\n".join(lines)

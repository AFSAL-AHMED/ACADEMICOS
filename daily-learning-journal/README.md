# 📖 Daily Learning Journal — MCP Server

A personal Notion MCP server to log, track, and review your daily learning.
No AI. Just you and your progress.

---

## 🚀 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure `.env`
```
NOTION_TOKEN=your_notion_integration_token
DATABASE_ID=your_database_id
```

- **NOTION_TOKEN** → Notion → Settings → Integrations → Your integration → Secret key
- **DATABASE_ID** → Open your Learning Logs database in Notion → copy the ID from the URL

### 3. Share the Notion database with your integration
Open the database in Notion → `...` → Connections → Select your integration

### 4. Run the MCP server
```bash
python server.py
```

---

## 🛠 Available Tools

| Tool | Description |
|---|---|
| `add_learning_log` | Add a new daily learning entry |
| `get_todays_log` | View today's log |
| `list_recent_logs` | See the last N days (default: 7) |
| `get_stats` | Overall stats — hours, topics, streak |
| `search_logs_by_topic` | Filter logs by topic |

---

## 📋 Database Properties

| Property | Type | Notes |
|---|---|---|
| Day | Title | e.g. "Day 1 — Python Basics" |
| Date | Date | Log date |
| Topic | Select | Programming, AI/ML, Web Dev, etc. |
| Hours Spent | Number | How many hours you studied |
| Mood | Select | 🔥 Fired Up / 😊 Good / 😐 Okay / 😴 Tired |
| Key Takeaways | Text | What you actually learned |
| Resources Used | Text | Books, videos, docs, links |
| Tomorrow's Goal | Text | What to tackle next |
| Streak Day | Number | Your current streak count |

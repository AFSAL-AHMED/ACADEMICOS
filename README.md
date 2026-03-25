# 🎓 ACADEMICOS — AI-Powered Academic Operating System

> Built for the **Notion MCP Challenge** — turning your syllabus into a fully automated Notion workspace using AI.

## 🚀 What It Does

**ACADEMICOS** (powered by ScholarAI) is an intelligent academic assistant that:

1. **📄 Parses your syllabus** (PDF or TXT) and extracts topics, deadlines, and assignments using a local LLM (Ollama)
2. **🤖 Syncs to Notion** via the **Notion MCP API** — automatically creating a structured study workspace with tasks, due dates, and priorities
3. **📚 Summarizes lecture notes** into AI-generated study guides
4. **⚙️ Adjusts your schedule** dynamically if you fall behind — it fetches your Notion tasks and recalculates priorities

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI / LLM | Ollama (`phi3:latest`) — runs **locally, no API cost** |
| Notion Integration | **Notion MCP API** (`notion-client`) |
| PDF Parsing | PyPDF |
| Language | Python 3.10+ |

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/AFSAL-AHMED/ACADEMICOS.git
cd ACADEMICOS
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your Notion API Key and Page ID
```

### 4. Pull the local LLM (Ollama)
```bash
# Install Ollama from https://ollama.com, then:
ollama pull phi3
```

### 5. Run the app
```bash
streamlit run app.py
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `NOTION_API_KEY` | Your Notion Internal Integration Secret (starts with `ntn_`) |
| `NOTION_PAGE_ID` | The 32-character ID from your Notion page URL |

> See `.env.example` for the template.

## 🏗️ Project Structure

```
ACADEMICOS/
├── app.py              # Streamlit UI — main entry point
├── agent.py            # ScholarAI agent — LLM + Notion MCP logic
├── parser.py           # Syllabus/PDF parser
├── prompts.py          # LLM prompt templates
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── sample_syllabus.txt # Sample syllabus for testing
```

## 🧠 How It Works (MCP Integration)

```
User uploads syllabus
       ↓
 Ollama LLM parses & structures tasks
       ↓
 Notion MCP API creates:
   ├── 📋 Task database with deadlines
   ├── 📅 Calendar entries
   └── 📝 Study notes pages
```

## 📸 Demo

Upload a syllabus → watch ScholarAI instantly build your entire Notion study workspace!

---

Made with ❤️ for the **Notion MCP Challenge**

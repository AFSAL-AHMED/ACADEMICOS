from flask import Flask, render_template, request, jsonify
from server import (
    add_learning_log,
    get_todays_log,
    list_recent_logs,
    get_stats,
    search_logs_by_topic,
)
from datetime import date
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion      = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("DATABASE_ID")
DS_ID       = "3540cab0-0e4d-80f4-aff4-000b79dce777"

app = Flask(__name__)


def _get_text(props, key):
    rt = props.get(key, {}).get("rich_text", [])
    return rt[0]["plain_text"] if rt else ""

def _get_select(props, key):
    sel = props.get(key, {}).get("select")
    return sel["name"] if sel else ""

def _get_title(props, key="Day"):
    t = props.get(key, {}).get("title", [])
    return t[0]["plain_text"] if t else ""

def _get_number(props, key):
    return props.get(key, {}).get("number") or 0

def _get_date(props):
    d = props.get("Date", {}).get("date")
    return d["start"] if d else ""


@app.route("/")
def index():
    return render_template("index.html", today=date.today().isoformat())


@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.json
    try:
        result = add_learning_log(
            day_title     = data.get("day_title", ""),
            topic         = data.get("topic", "Other"),
            hours_spent   = float(data.get("hours_spent", 1)),
            mood          = data.get("mood", "Good"),
            key_takeaways = data.get("key_takeaways", ""),
            resources_used= data.get("resources_used", ""),
            tomorrows_goal= data.get("tomorrows_goal", ""),
            streak_day    = int(data.get("streak_day", 1)),
            log_date      = data.get("log_date", ""),
        )
        return jsonify({"success": True, "message": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/logs")
def api_logs():
    try:
        limit = int(request.args.get("limit", 10))
        res   = notion.request(
            path=f"data_sources/{DS_ID}/query",
            method="POST",
            body={
                "sorts": [{"property": "Date", "direction": "descending"}],
                "page_size": limit,
            },
        )
        entries = []
        for page in res.get("results", []):
            p = page["properties"]
            entries.append({
                "id":            page["id"],
                "url":           page.get("url", ""),
                "day":           _get_title(p),
                "date":          _get_date(p),
                "topic":         _get_select(p, "Topic"),
                "hours":         _get_number(p, "Hours Spent"),
                "mood":          _get_select(p, "Mood"),
                "streak":        _get_number(p, "Streak Day"),
                "takeaways":     _get_text(p, "Key Takeaways"),
                "resources":     _get_text(p, "Resources Used"),
                "tomorrows_goal":_get_text(p, "Tomorrow's Goal"),
            })
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats")
def api_stats():
    try:
        res   = notion.request(
            path=f"data_sources/{DS_ID}/query",
            method="POST",
            body={"sorts": [{"property": "Date", "direction": "descending"}]},
        )
        pages = res.get("results", [])
        if not pages:
            return jsonify({"total_days": 0, "total_hours": 0, "max_streak": 0, "topics": {}})

        total_hours, topic_counts, max_streak = 0, {}, 0
        for page in pages:
            p = page["properties"]
            total_hours += _get_number(p, "Hours Spent")
            t = _get_select(p, "Topic")
            if t:
                topic_counts[t] = topic_counts.get(t, 0) + 1
            s = _get_number(p, "Streak Day")
            if s > max_streak:
                max_streak = s

        return jsonify({
            "total_days":  len(pages),
            "total_hours": round(total_hours, 1),
            "max_streak":  max_streak,
            "topics":      topic_counts,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050)

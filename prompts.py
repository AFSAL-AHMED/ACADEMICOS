"""
prompts.py

System and User prompts for interacting with the local LLM via Ollama.
"""

SYLLABUS_EXTRACTION_PROMPT = """
You are an expert academic assistant. Your job is to read a college course syllabus and extract key actionable information.
Please extract the following details and output them strictly as a formatted JSON array of tasks exactly as follows, with no extra text or markdown code blocks:
[
  {{
    "task": "Read Chapter 1",
    "deadline_date": "2026-03-20",
    "type": "Reading"
  }},
  {{
    "task": "Midterm Exam",
    "deadline_date": "2026-04-15",
    "type": "Exam"
  }}
]

Syllabus Text:
{syllabus_text}
"""

STUDY_PLANNER_PROMPT = """
You are an expert study planner. Given the following extracted deadlines from a syllabus, break them down into a daily/weekly schedule. 
For each major exam or assignment, create 2-3 smaller milestone tasks leading up to it.

Output strictly as a formatted JSON array of tasks:
[
  {{
    "task": "Milestone: Draft Outline for Essay 1",
    "deadline_date": "2026-03-10",
    "type": "Milestone"
  }}
]

Deadlines:
{deadlines_json}
"""

BEHIND_SCHEDULE_PROMPT = """
You are an adaptive AI academic assistant. The student is currently behind schedule and missed the deadlines for their study plan.
Please adjust their deadlines in the provided list to shift them forward by 2-3 days securely. Ensure all generated dates are realistic and in YYYY-MM-DD format.

Output strictly as a JSON array of the updated tasks containing 'id', 'task', 'type' and the new 'deadline_date'. Maintain the format exactly.
Do not output any additional conversational text.

Current Tasks:
{tasks_json}
"""

SUMMARIZE_NOTES_PROMPT = """
You are an expert AI tutor. Summarize the provided lecture notes into a structured study guide.
Highlight the absolute most critical concepts suitable for exam revision.
Return the output formatted in Markdown, specifically using headings, bullet points, and bold text for key terms.

Lecture Notes:
{notes_text}
"""

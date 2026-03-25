"""
agent.py

The ScholarAI Agent. Connects to Local Ollama for AI logic 
and the Notion MCP server for workspace automation.
"""

import os
import json
import asyncio
from typing import List, Dict

import ollama
from notion_client import Client
from dotenv import load_dotenv

import prompts
from parser import extract_text_from_file

load_dotenv()

OLLAMA_MODEL = "phi3:latest"
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")


def call_local_llm(prompt: str) -> str:
    """Wrapper to call Ollama locally."""
    print(f"Calling Ollama ({OLLAMA_MODEL}) with prompt of length {len(prompt)}...")
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "[]"

def parse_json_from_llm(text: str) -> List[Dict]:
    """Helper to clean up output from local LLMs which might not strictly follow JSON."""
    try:
        # Find first [ and last ]
        start = text.find('[')
        end = text.rfind(']') + 1
        if start != -1 and end != 0:
            json_str = text[start:end]
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from LLM: {e}")
        print("Raw output:", text)
    return []

class ScholarAI:
    def __init__(self):
        self.notion_page_id = NOTION_PAGE_ID
        
        if not self.notion_page_id or not NOTION_API_KEY:
            raise ValueError("Missing NOTION_API_KEY or NOTION_PAGE_ID in .env file.")

    def process_syllabus(self, file_path: str) -> List[Dict]:
        """Reads a syllabus, extracts tasks, and generates a study plan."""
        print(f"Processing syllabus: {file_path}")
        text = extract_text_from_file(file_path)
        if not text:
            return []
            
        # 1. Extract Deadlines
        print("Extracting deadliness...")
        extraction_prompt = prompts.SYLLABUS_EXTRACTION_PROMPT.format(syllabus_text=text[:3000]) # Truncate for local LLM context
        raw_extraction = call_local_llm(extraction_prompt)
        deadlines = parse_json_from_llm(raw_extraction)
        
        # 2. Generate Study Plan
        print("Generating study plan milestones...")
        planner_prompt = prompts.STUDY_PLANNER_PROMPT.format(deadlines_json=json.dumps(deadlines))
        raw_plan = call_local_llm(planner_prompt)
        milestones = parse_json_from_llm(raw_plan)
        
        all_tasks = deadlines + milestones
        return all_tasks
        
    def sync_to_notion(self, tasks: List[Dict]):
        """
        Uses Notion API to write tasks into the workspace.
        This will create a new Database in the target page and add tasks.
        """
        import time
        import requests
        print(f"Syncing {len(tasks)} tasks to Notion Page: {self.notion_page_id}...")
        
        # 1. Create a Database using direct requests (more reliable for schema creation)
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        db_title = f"ScholarAI Plan - {int(time.time())}"
        payload = {
            "parent": {"type": "page_id", "page_id": self.notion_page_id},
            "title": [{"type": "text", "text": {"content": db_title}}],
            "properties": {
                "Name": {"title": {}},
                "Type": {"select": {}},
                "Deadline": {"date": {}},
                "Status": {"checkbox": {}}
            }
        }
        
        try:
            db_response = requests.post("https://api.notion.com/v1/databases", headers=headers, json=payload)
            if db_response.status_code >= 400:
                print(f"Error creating database: {db_response.text}")
                return False
                
            db_id = db_response.json()["id"]
            print(f"Created new Notion Database ({db_id}). Waiting for API sync...")
            time.sleep(2)
            
            # 2. Add all tasks into the new database (Using notion-client for insertion)
            notion = Client(auth=NOTION_API_KEY)
            for task in tasks:
                try:
                    task_name = task.get("task") or task.get("Task") or "Untitled"
                    task_type = task.get("type") or task.get("Type") or "General"
                    task_date = task.get("deadline_date") or task.get("deadline") or "2026-03-31"

                    notion.pages.create(
                        parent={"database_id": db_id},
                        properties={
                            "Name": {
                                "title": [{"text": {"content": task_name}}]
                            },
                            "Type": {
                                "select": {"name": task_type}
                            },
                            "Deadline": {
                                "date": {"start": task_date}
                            }
                        }
                    )
                    print(f" -> Created Notion Task: {task_name}")
                except Exception as task_err:
                    print(f" -> Failed to create task '{task_name}': {task_err}")
                
            print(f"Successfully synced to Notion! DB Name: {db_title}")
            return True
        except Exception as e:
            print(f"Error in sync process: {e}")
            return False

    def summarize_notes(self, file_path: str) -> str:
        """Reads lecture notes and generates a markdown summary."""
        print(f"Summarizing notes: {file_path}")
        text = extract_text_from_file(file_path)
        if not text:
            return "Could not read notes."
        
        prompt = prompts.SUMMARIZE_NOTES_PROMPT.format(notes_text=text[:4000])
        summary = call_local_llm(prompt)
        return summary
        
    def adjust_schedule(self) -> str:
        """
        Fetches current tasks from Notion Database, asks LLM to push deadlines back, 
        and updates the Notion DB with the new dates.
        """
        print("Adjusting schedule...")
        notion = Client(auth=NOTION_API_KEY)
        
        # 1. Fetch current tasks from the database (We assume the first DB in the page is ours for simplicity)
        try:
            databases = notion.search(query="ScholarAI Study Plan", filter={"value": "database", "property": "object"}).get("results")
            if not databases:
                return "Could not find ScholarAI Study Plan database in Notion."
            
            db_id = databases[0]["id"]
            
            # Get pages in DB
            pages = notion.databases.query(database_id=db_id).get("results")
            
            tasks = []
            for p in pages:
                # Extract simple task structure
                props = p["properties"]
                title_arr = props.get("Task", {}).get("title", [])
                task_name = title_arr[0]["text"]["content"] if title_arr else "Untitled"
                
                date_val = props.get("Deadline", {}).get("date", {})
                deadline = date_val.get("start") if date_val else "2026-01-01"
                
                type_val = props.get("Type", {}).get("select", {})
                task_type = type_val.get("name") if type_val else "General"
                
                tasks.append({
                    "id": p["id"],
                    "task": task_name,
                    "deadline_date": deadline,
                    "type": task_type
                })
                
            if not tasks:
                return "Database is empty."
                
            # 2. Ask LLM to adjust
            print(f"Asking LLM to adjust {len(tasks)} tasks...")
            prompt = prompts.BEHIND_SCHEDULE_PROMPT.format(tasks_json=json.dumps(tasks))
            raw_adjusted = call_local_llm(prompt)
            adjusted_tasks = parse_json_from_llm(raw_adjusted)
            
            if not adjusted_tasks:
                return "Failed to parse adjusted tasks from AI."
                
            # 3. Update Notion
            for task in adjusted_tasks:
                page_id = task.get("id")
                new_date = task.get("deadline_date")
                if page_id and new_date:
                    notion.pages.update(
                        page_id=page_id,
                        properties={
                            "Deadline": {
                                "date": {"start": new_date}
                            }
                        }
                    )
                    
            return f"Successfully pushed forward deadlines for {len(adjusted_tasks)} tasks in Notion!"
            
        except Exception as e:
            print(f"Error adjusting schedule: {e}")
            return f"Error connecting to Notion: {str(e)}"

# Simple test block:
if __name__ == "__main__":
    agent = ScholarAI()
    print("Agent initialized successfully.")

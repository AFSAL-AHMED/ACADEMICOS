import os
import time
import tempfile
import streamlit as st

from dotenv import load_dotenv

from agent import ScholarAI

load_dotenv()

st.set_page_config(page_title="ScholarAI 🎓", layout="wide")

st.title("🎓 ScholarAI: Your Academic Operating System")
st.markdown("Automate your study planning and Notion workspace directly from your syllabus.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Workspace Config")
    st.markdown("**Notion Page ID:**")
    st.code(os.getenv("NOTION_PAGE_ID", "Not found in .env"))
    
    st.markdown("**LLM Engine:**")
    st.code("Ollama (phi3:latest)")

st.header("1. Upload Syllabus")
uploaded_file = st.file_uploader("Upload your course syllabus (.pdf or .txt)", type=['pdf', 'txt'])

if uploaded_file is not None:
    st.success(f"Uploaded {uploaded_file.name} successfully!")
    
    # Save the uploaded file temporarily so the backend can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    if st.button("▶️ Generate Study Plan & Sync to Notion"):
        try:
            agent = ScholarAI()
            
            with st.spinner("🧠 AI Reading Syllabus & Extracting Deadlines..."):
                time.sleep(1) # Visual UI buffer
                tasks = agent.process_syllabus(tmp_path)
            
            if not tasks:
                st.error("Failed to generate any tasks. Check the terminal logs.")
            else:
                st.write("### AI Generated Plan:")
                st.json(tasks)
                
                with st.spinner("🤖 Syncing Tasks to Notion MCP Workspace..."):
                    agent.sync_to_notion(tasks)
                    time.sleep(1)
                
                st.success("✅ Success! Your academic workspace in Notion has been updated.")
                st.balloons()
            
        except Exception as e:
            st.error(f"Error during Processing: {e}")
        finally:
            os.remove(tmp_path)

st.divider()
st.header("2. Lecture Note Summarizer")
st.markdown("Upload your lecture notes (PDF/txt) to get an AI-generated study guide.")

notes_file = st.file_uploader("Upload lecture notes", type=['pdf', 'txt'], key="notes_uploader")
if notes_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{notes_file.name.split('.')[-1]}") as notes_tmp:
        notes_tmp.write(notes_file.getvalue())
        notes_path = notes_tmp.name
        
    if st.button("📝 Generate Study Guide"):
        try:
            agent = ScholarAI()
            with st.spinner("🧠 AI Summarizing Notes..."):
                summary = agent.summarize_notes(notes_path)
            st.markdown("### 📚 Study Guide")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Error during Summarization: {e}")
        finally:
            os.remove(notes_path)

st.divider()
st.header("3. Manage Schedule (Advanced Feature)")
st.markdown("Are you falling behind? Use ScholarAI to dynamically adjust your deadlines.")

if st.button("⚠️ I'm Behind Schedule - Adjust My Plan"):
    try:
        agent = ScholarAI()
        with st.spinner("🧠 AI Fetching tasks from Notion and recalculating priorities..."):
            result = agent.adjust_schedule()
        if "Error" in result or "Could not" in result or "Failed" in result:
             st.error(result)
        else:
             st.success(result)
             st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")

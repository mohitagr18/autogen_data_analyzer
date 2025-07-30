import streamlit as st
import asyncio
import os
from pathlib import Path
from teams.analyzer_team import get_data_analyzer_team
from models.openai_model_client import get_model_client
# from config.docker_util import get_docker_executor, start_docker_executor, stop_docker_executor
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from autogen_agentchat.

# Use Constants for paths and filenames
TEMP_DIR = Path("temp")
INPUT_CSV_PATH = TEMP_DIR / "data.csv"
REPORT_MD_PATH = TEMP_DIR / "report.md"

def initialize_state():
    """Initializes session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'team_state' not in st.session_state:
        st.session_state.team_state = None
    if 'report_content' not in st.session_state:
        st.session_state.report_content = None

def prepare_task_environment(uploaded_file):
    """Creates temp dir, saves uploaded file, and resets state for new file."""
    TEMP_DIR.mkdir(exist_ok=True)
    
    # If a new file is uploaded, clear the old report from the session state
    if 'uploaded_file_name' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.report_content = None
        st.session_state.uploaded_file_name = uploaded_file.name

    with open(INPUT_CSV_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
                
    return set(TEMP_DIR.glob('*.png'))

async def display_streamed_messages(team_run_stream):
    """Renders messages from the agent team stream into the Streamlit UI."""
    message_map = {
        "user": ("User", "👤"),
        "Data_Analyzer": ("Data Analyzer", "🤖"),
        "Python_Code_Executor": ("Python Code Executor", "🐍"),
    }
    
    async for message in team_run_stream:
        if isinstance(message, TextMessage):
            # Find the role and avatar for the message source
            for key, (role, avatar) in message_map.items():
                if message.source.startswith(key):
                    with st.chat_message(role, avatar=avatar):
                        st.markdown(message.content)
                    break
            st.session_state.messages.append(message.content)
        elif isinstance(message, TaskResult):
            st.markdown(f"Stop Reason: {message.stop_reason}")
            st.session_state.messages.append(message.stop_reason)

# async def run_analysis_task(model_client, docker_executor, task):
async def run_analysis_task(model_client, code_executor, task):

    """Handles the full lifecycle of running the AutoGen team."""
    try:
        # await start_docker_executor(docker_executor)
        # team = get_data_analyzer_team(model_client, docker_executor)
        team = get_data_analyzer_team(model_client, code_executor)

        if st.session_state.team_state:
            await team.load_state(st.session_state.team_state)

        team_stream = team.run_stream(task=task)
        await display_streamed_messages(team_stream)

        st.session_state.team_state = await team.save_state()
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        pass
        # await stop_docker_executor(docker_executor)

def display_task_results(existing_pngs):
    """Displays the final artifacts (report or images) after a task."""
    if REPORT_MD_PATH.is_file():
        st.markdown("---")
        st.subheader("📊 Generated Data Analysis Report")
        report_content = REPORT_MD_PATH.read_text()
        st.markdown(report_content, unsafe_allow_html=True)
    else:
        # Find and display only newly created PNG files
        current_pngs = set(TEMP_DIR.glob('*.png'))
        new_pngs = current_pngs - existing_pngs
        if new_pngs:
            for image_path in new_pngs:
                st.image(str(image_path), caption=f'Generated Plot: {image_path.name}')
        else:
            st.success("Task completed!")

# --- Main Application ---
st.title("AutoGen Data Analyst: A Multi-Agent AI Application")
st.markdown("This application leverages a team of AI agents to perform on-the-fly data analysis. Users can watch in real-time as the agents collaborate to automatically write and execute Python code, generating instant insights, plots, and full reports from any uploaded CSV file.")

initialize_state()

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
task = st.chat_input("Enter your task here...")

# Display chat history
for msg in st.session_state.messages:
    st.markdown(msg)

if task and uploaded_file:
    existing_pngs = prepare_task_environment(uploaded_file)
    
    # docker_executor = get_docker_executor()
    code_executor = LocalCommandLineCodeExecutor(work_dir=TEMP_DIR)
    model_client = get_model_client()
    
    # asyncio.run(run_analysis_task(model_client, docker_executor, task))
    asyncio.run(run_analysis_task(model_client, code_executor, task))
    
    display_task_results(existing_pngs)
elif task:
    st.warning("Please upload a CSV file first.")
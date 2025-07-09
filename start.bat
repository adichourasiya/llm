@echo off
REM Activate the virtual environment (if exists)
IF EXIST .venv\Scripts\activate (
    call .venv\Scripts\activate
)

REM Set environment variables from .env if needed (python-dotenv handles this in app)

REM Run Streamlit app
streamlit run g:\AI\local_llm\llm\app.py

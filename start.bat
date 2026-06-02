@echo off
echo ===================================================
echo     Starting QEC Auto-Filler Application
echo ===================================================

:: Check if virtual environment exists, if not create it
if not exist venv (
    echo [1/4] Creating Python virtual environment...
    python -m venv venv
) else (
    echo [1/4] Virtual environment found.
)

:: Activate the virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo [3/4] Checking and installing requirements...
pip install -r requirements.txt
playwright install

:: Start the application
echo [4/4] Starting the Flask Web Server...
echo The application will be available at http://localhost:5000
echo Keep this window open to keep the server running.
echo ===================================================

:: Automatically open the default browser to the web app
start http://localhost:5000

:: Run the app
python app.py
pause

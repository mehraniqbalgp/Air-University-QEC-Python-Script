# QEC Automation Web App

A full-stack web application designed for securely automating QEC (Quality Enhancement Cell) surveys on the Air University portal. 

The tool now features a premium "Glassmorphism" UI and handles requests in the background asynchronously. Multiple users can submit their credentials simultaneously without their passwords ever being saved, logged, or revealed to others. You can even see a live streaming terminal in your browser of the automation completing its tasks!

## Prerequisites

- Python 3.7+
- Playwright
- Flask

## One-Command Installation & Run

You can download, set up, and launch the application in a single command. This will automatically clone the repository, install all dependencies, and open the web app.

**For Linux / macOS:**
Open your terminal and paste this command:
```bash
git clone https://github.com/mehraniqbalgp/Air-University-QEC-Python-Script.git && cd Air-University-QEC-Python-Script && chmod +x start.sh && ./start.sh
```

**For Windows:**
Open your Command Prompt (cmd) and paste this command:
```cmd
git clone https://github.com/mehraniqbalgp/Air-University-QEC-Python-Script.git && cd Air-University-QEC-Python-Script && start.bat
```

*(Note: You must have [Git](https://git-scm.com/) installed on your system to use these commands. Once the script finishes, your default web browser will automatically open the application at `http://localhost:5000`.)*

## Manual Installation & Usage

If you prefer to set up the environment manually:

1. Clone the repository and navigate into the directory.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to `http://localhost:5000`.

## Features
- **Concurrent Execution:** Safely spawns independent headless browser processes in the background. Multiple users can automate their surveys at the same time.
- **Privacy & Security:** Credentials are passed directly to the automation engine in memory and are wiped immediately from the UI upon submission.
- **Real-Time Logging:** See the status of your task via Server-Sent Events (SSE) directly in the UI.

## Disclaimer

This tool is for educational purposes and personal automation. Use it responsibly and ensure you comply with your university's policies.

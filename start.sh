#!/bin/bash
echo "==================================================="
echo "    Starting QEC Auto-Filler Application"
echo "==================================================="

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment found."
fi

# Activate the virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[3/4] Checking and installing requirements..."
pip install -r requirements.txt
playwright install

# Start the application
echo "[4/4] Starting the Flask Web Server..."
echo "The application will be available at http://localhost:5000"
echo "Keep this terminal open to keep the server running."
echo "==================================================="

# Try to automatically open the default browser to the web app
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &> /dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:5000 &> /dev/null &
fi

# Run the app
python app.py

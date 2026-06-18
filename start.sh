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

# Playwright 1.60 does not yet ship ubuntu26.04 browser builds; use 24.04 binaries.
if [ -f /etc/os-release ] && grep -q 'VERSION_ID="26.04"' /etc/os-release; then
    export PLAYWRIGHT_HOST_PLATFORM_OVERRIDE="${PLAYWRIGHT_HOST_PLATFORM_OVERRIDE:-ubuntu24.04-x64}"
    echo "Ubuntu 26.04 detected — using Playwright ubuntu24.04 browser builds."
fi

if ! playwright install chromium; then
    echo "Warning: Playwright browser install failed."
    if command -v google-chrome &>/dev/null || command -v google-chrome-stable &>/dev/null; then
        echo "System Google Chrome found — automation will use it instead."
    else
        echo "Install Google Chrome, or run:"
        echo "  PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64 playwright install chromium"
    fi
fi

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

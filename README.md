# QEC Automation

Automated script for filling out QEC (Quality Enhancement Cell) surveys on the university portal.

## Prerequisities

- Python 3.7+
- Playwright

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install the Playwright browsers:

```bash
playwright install
```

## Usage

1. Open `qec_auto.py` and update the credentials if necessary (Note: It is recommended to use environment variables for security).
2. Run the script:

```bash
python qec_auto.py
```

The script will launch a browser (non-headless by default), log in to the portal, and automatically fill out the available evaluations for courses, teachers, and online learning feedback.

## Disclaimer

This tool is for educational purposes and personal automation. Use it responsibly and ensure you comply with your university's policies.

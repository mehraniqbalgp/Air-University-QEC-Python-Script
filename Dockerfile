# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Prevent apt-get from prompting for user input during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Playwright and Xvfb before switching user
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    xvfb \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies globally so Playwright CLI is available
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Playwright system dependencies (run as root)
RUN playwright install-deps

# Create a non-root user with UID 1000 (Required by Hugging Face Spaces)
RUN useradd -m -u 1000 user

# Switch to the non-root user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Install Playwright chromium for the user
RUN playwright install chromium

# Copy the rest of the application and set ownership to 'user'
COPY --chown=user . /app

# Expose port 7860 (Required by Hugging Face Spaces)
EXPOSE 7860

# Run the app directly
CMD gunicorn --bind 0.0.0.0:7860 --workers 1 --threads 4 app:app

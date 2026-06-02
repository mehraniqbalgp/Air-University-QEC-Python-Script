# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies (plus gunicorn for production)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Playwright and its system dependencies
# We only install chromium to keep the image lightweight
RUN playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Expose port 5000 (standard for Flask)
EXPOSE 5000

# Run the app using Gunicorn (production server) instead of the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "app:app"]

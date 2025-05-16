# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
# Exit on errors, no .pyc files, unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (if any) and Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port 5000 for Flask
EXPOSE 8080

# Tell Flask how to start
ENV FLASK_APP=run.py \
    FLASK_ENV=production

# Default command
CMD ["python", "run.py"]

# Use Python 3.9 base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    wget \
    unzip \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask port
EXPOSE 10000

# Use /tmp for session storage to avoid SQLite errors
ENV TMPDIR=/tmp

# Start the app: Flask on port 10000 and Pyrogram bot
CMD flask run -h 0.0.0.0 -p 10000 & python3 main.py

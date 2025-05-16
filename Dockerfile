FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY uv.lock .

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system .

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Command to run the application
CMD ["python", "main.py"] 
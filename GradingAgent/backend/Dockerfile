# Base image
FROM python:3.11-slim

# System/runtime hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install build dependencies and Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["/root/.local/bin/uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]
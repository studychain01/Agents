# ---------- base image ----------
FROM python:3.11-slim

# System/runtime hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["python", "-m", "uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]
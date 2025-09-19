# ---------- base image ----------
    FROM python:3.11-slim

    # System/runtime hygiene
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PIP_NO_CACHE_DIR=1
    
    WORKDIR /app
    
    # (Optional) build tools if any wheel needs compiling
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*
    
    # Install Python deps first (better layer caching)
    COPY requirements.txt .
    RUN pip install --upgrade pip && pip install -r requirements.txt
    
    # Copy the rest of your code
    COPY . .
    
    # Expose FastAPI port
    EXPOSE 8000
    
    # If your FastAPI instance is named `app` in main.py:
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    
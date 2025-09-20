# ---- base build stage ----
    FROM python:3.12-slim AS base

    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PIP_NO_CACHE_DIR=1
    
    # System deps (add build tools only if you need them)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
        rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Copy only requirements first (better caching)
    COPY requirements.txt .
    
    RUN pip install --upgrade pip && \
        pip install -r requirements.txt
    
    # ---- runtime stage ----
    FROM python:3.12-slim AS runtime
    
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1
    
    # Create non-root user
    RUN useradd -m -u 10001 appuser
    
    WORKDIR /app
    COPY --from=base /usr/local/lib/python3.12 /usr/local/lib/python3.12
    COPY --from=base /usr/local/bin /usr/local/bin
    
    # Copy source
    COPY . /app
    
    # Expose FastAPI port
    EXPOSE 8000
    
    # Healthcheck (adjust path if you add /health)
    HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
      CMD curl -fsS http://127.0.0.1:8000/docs || exit 1
    
    USER appuser
    
    # Start server (replace module path if your file isn't app.py or app object isn't fastapi_app)
    # Here we assume app.py defines: fastapi_app = FastAPI(...)
    CMD ["uvicorn", "app:fastapi_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
    
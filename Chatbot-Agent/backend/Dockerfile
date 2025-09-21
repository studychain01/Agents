# NEW DOCKERFILE - FORCE REBUILD
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 appuser

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip list | grep uvicorn

# Copy application code
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8080/health || exit 1

# Switch to non-root user
USER appuser

# Verify uvicorn is available
RUN which uvicorn && uvicorn --version

# Start application
CMD ["uvicorn", "app:fastapi_app", "--host", "0.0.0.0", "--port", "8080"]

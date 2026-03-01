# Multi-stage Dockerfile for SprintSync API
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Production stage ---
FROM python:3.11-slim

WORKDIR /app

# Install runtime deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

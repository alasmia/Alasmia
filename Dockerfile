# =============================================================================
# Alasmia Docker Container
# =============================================================================
# Multi-stage build for minimal image size

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Set environment
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data

# Expose port for web UI (if enabled)
EXPOSE 8000

# Run Alasmia
CMD ["python", "main.py"]

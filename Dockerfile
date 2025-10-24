# Sorisay AI Application Dockerfile
# Multi-stage build for optimized image size

# Stage 1: Build stage
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.10-slim

LABEL maintainer="parkcheolhong"
LABEL description="신세계 투사이클 소리새 브레인 시스템"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    espeak \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY modules/ ./modules/
COPY config/ ./config/
COPY run_all_shinsegye.py .
COPY requirements.txt .
COPY README.md .
COPY QUICKSTART.md .
COPY SECURITY.md .

# Create necessary directories with proper permissions
RUN mkdir -p logs data memories backups \
    && chmod -R 755 logs data memories backups

# Expose port for web dashboard
EXPOSE 5050

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run the application as non-root user for security
RUN useradd -m -u 1000 sorisay && \
    chown -R sorisay:sorisay /app
USER sorisay

# Run the application
CMD ["python", "run_all_shinsegye.py"]

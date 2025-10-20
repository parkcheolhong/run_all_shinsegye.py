# Sorisay AI Application Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for audio processing
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data memories config

# Expose port for web dashboard
EXPOSE 5050

# Set environment variable for unbuffered Python output
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "run_all_shinsegye.py"]

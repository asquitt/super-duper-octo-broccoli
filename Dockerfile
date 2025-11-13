# Multimodal Clip Extractor - Docker Image
# Optimized for CPU-only processing

FROM python:3.9-slim

LABEL maintainer="your-email@example.com"
LABEL description="Multimodal AI-powered video clip extractor"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libgomp1 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements-minimal.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/temp /app/cache /app/models /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CLIP_EXTRACTOR_TEMP_DIR=/app/temp
ENV CLIP_EXTRACTOR_CACHE_DIR=/app/cache

# Make main.py executable
RUN chmod +x main.py

# Volume mounts for input/output
VOLUME ["/input", "/output"]

# Default command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]

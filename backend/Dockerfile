FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including build tools for compiling packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cmake \
    git \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (use --pre for pre-release packages like httpx 1.0)
# Install an older pip (24.x) that handles build isolation better with openai-whisper
# Also install wheel which is needed for building
# Install setuptools first (needed for building packages like openai-whisper)
RUN pip install --upgrade "pip<25" wheel setuptools && \
    pip install --no-cache-dir --pre -r requirements.txt && \
    # Install openai-whisper. We use --no-build-isolation to avoid isolated build environment
    # that would fail due to missing pkg_resources (setuptools)
    pip install --no-cache-dir --no-build-isolation --force-reinstall --no-deps openai-whisper==20250625 || true

# Copy application code
COPY app ./app

# Create directory for uploaded files
RUN mkdir -p /tmp/transcriber

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Run the application

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
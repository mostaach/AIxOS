# AIxOS Dockerfile
# Multi-stage build for better security and smaller image size
FROM ubuntu:22.04 AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    nano \
    sudo \
    htop \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r aixos && useradd -r -g aixos -u 1000 aixos

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/config && \
    chown -R aixos:aixos /app

# Production stage
FROM base AS production

# Copy application code
COPY --chown=aixos:aixos . .

# Switch to non-root user
USER aixos

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import aixos; print('AIxOS is healthy')" || exit 1

# Set the entrypoint
ENTRYPOINT ["python3", "aixos/main.py"]

# Development stage
FROM base AS development

# Install additional development tools
RUN apt-get update && apt-get install -y \
    vim \
    tmux \
    fish \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip3 install --no-cache-dir \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

# Copy application code
COPY --chown=aixos:aixos . .

# Switch to non-root user
USER aixos

# Default to bash for development
CMD ["/bin/bash"]
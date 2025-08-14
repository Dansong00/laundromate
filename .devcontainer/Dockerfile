FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments (since we're in a container)
RUN poetry config virtualenvs.create false

# Set working directory
WORKDIR /workspace

# Set environment variables
ENV PYTHONPATH=/workspace/apps/api
ENV PYTHONUNBUFFERED=1

# Keep container running
CMD ["sleep", "infinity"]

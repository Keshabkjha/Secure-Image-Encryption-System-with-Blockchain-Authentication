# Build stage for Python dependencies
FROM python:3.8-slim as python-base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Build stage for Node.js
FROM node:16-slim as node-base

WORKDIR /app

# Copy package files
COPY Backend/package*.json ./Backend/

# Install Node.js dependencies
RUN cd Backend && npm install --production

# Final stage
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=python-base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=python-base /usr/local/bin /usr/local/bin

# Copy Node.js dependencies
COPY --from=node-base /app/Backend/node_modules /app/Backend/node_modules

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Expose ports
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PYTHONPATH=/app

# Set the command to run the application
CMD ["sh", "-c", "cd Backend && node server.js"]

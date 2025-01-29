# backend/Dockerfile
FROM python:3.10-slim as builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /backend
WORKDIR /backend

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the application files
COPY ./app ./app
COPY ./data ./data

# Expose the FastAPI port
EXPOSE 8080

# Run FastAPI with Uvicorn (from the backend folder)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
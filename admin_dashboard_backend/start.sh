#!/bin/bash

# Startup script for FastAPI backend

echo "Starting Fashion & Lifestyle Admin Dashboard Backend..."

# Set working directory
cd "$(dirname "$0")"

# Check if database needs initialization
if [ ! -f ".db_initialized" ]; then
    echo "Initializing database with sample data..."
    python -m src.init_db
    if [ $? -eq 0 ]; then
        touch .db_initialized
        echo "Database initialized successfully!"
    else
        echo "Warning: Database initialization failed. Continuing anyway..."
    fi
else
    echo "Database already initialized. Skipping initialization..."
fi

# Generate OpenAPI specification
echo "Generating OpenAPI specification..."
python -m src.api.generate_openapi

# Start the server
echo "Starting FastAPI server on port ${PORT:-3001}..."
uvicorn src.api.main:app --host ${UVICORN_HOST:-0.0.0.0} --port ${PORT:-3001} --reload

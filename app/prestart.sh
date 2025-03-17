#!/bin/bash

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000

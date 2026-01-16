#!/bin/bash

# Start the Test Case Generator Service

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if required environment variables are set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY is not set in .env"
    exit 1
fi

echo "Starting Test Case Generator Service..."
echo "Service will be available at http://localhost:${SERVICE_PORT:-8000}"
echo "API Documentation at http://localhost:${SERVICE_PORT:-8000}/docs"

# Run the service
python -m uvicorn app.main:app --host 0.0.0.0 --port ${SERVICE_PORT:-8000} --reload

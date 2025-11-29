#!/bin/bash
set -e

echo "=================================="
echo "Starting Backend Initialization"
echo "=================================="

# Initialize database (create tables)
echo "Initializing database..."
python init_db.py

echo ""
echo "=================================="
echo "Starting API Server"
echo "=================================="

# Start the API server
exec uvicorn Backend.api:app --reload --host 0.0.0.0 --port 8000

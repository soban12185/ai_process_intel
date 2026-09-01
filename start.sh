#!/bin/bash
# Startup script for Render deployment
# Seeds database on first run, then starts the server

echo "Starting NovaBank AI Process Intelligence Engine..."

# Create data directory
mkdir -p data

# Check if database exists, if not seed it
if [ ! -f data/modus_ai.db ]; then
    echo "Database not found. Seeding..."
    python seed/seed.py
    echo "Database seeded successfully."
else
    echo "Database already exists."
fi

# Start the server
echo "Starting server..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}

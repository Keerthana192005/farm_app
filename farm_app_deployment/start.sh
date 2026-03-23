#!/bin/bash
# Farm App Startup Script
echo "Starting Farm Fresh Vegetables App..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/uploads
mkdir -p instance

# Initialize database
python -c "from app import create_tables_and_seed; create_tables_and_seed()"

# Start the application
echo "App starting on http://localhost:5000"
python run.py

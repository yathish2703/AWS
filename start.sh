#!/bin/bash

# AWS Learning Platform - Start Script

echo "🚀 Starting AWS Learning Platform..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Stop any existing instances
echo "Stopping existing instances..."
pkill -f "python app.py" 2>/dev/null

sleep 2

# Start Flask application
echo ""
echo "✅ Starting Flask server on port 5001..."
echo ""
python app.py

echo ""
echo "Server stopped."

#!/bin/bash
echo "Starting Sydney Events Scraper Backend..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo
    echo "Installing Playwright browsers..."
    playwright install chromium
    echo
    echo "Setup complete! Starting server..."
    echo
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo
echo "========================================"
echo "Backend Server Starting..."
echo "========================================"
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo

python -m app.main


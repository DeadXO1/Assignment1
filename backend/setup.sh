#!/bin/bash
# Setup script for backend

echo "Setting up Sydney Events Scraper Backend..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

echo "Backend setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To start the server, run: python -m app.main"


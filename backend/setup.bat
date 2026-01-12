@echo off
REM Setup script for backend (Windows)

echo Setting up Sydney Events Scraper Backend...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Install Playwright browsers
playwright install chromium

echo Backend setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate
echo To start the server, run: python -m app.main


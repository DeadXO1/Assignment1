@echo off
echo Starting Sydney Events Scraper Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
    echo Installing Playwright browsers...
    playwright install chromium
    echo.
    echo Setup complete! Starting server...
    echo.
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo ========================================
echo Backend Server Starting...
echo ========================================
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m app.main

pause


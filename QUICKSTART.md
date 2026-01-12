# Quick Start Guide

## Prerequisites
- Python 3.11 or higher installed
- Node.js 18 or higher installed
- npm (comes with Node.js)

## Step 1: Backend Setup

### Windows:
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for scraping)
playwright install chromium

# Create .env file (optional - defaults work for localhost)
# Copy .env.example to .env if you want to customize settings

# Start the backend server
python -m app.main
```

### macOS/Linux:
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Start the backend server
python -m app.main
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The API will be available at: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

## Step 2: Frontend Setup (in a new terminal)

### Windows:
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### macOS/Linux:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

The frontend will be available at: **http://localhost:5173**

## Step 3: Using the Application

1. **Open your browser** and go to `http://localhost:5173`
2. **Wait for events to load** - The scrapers run automatically when the backend starts
3. **Browse events** - You'll see event cards with images, titles, dates, and locations
4. **Search/Filter** - Use the search bar and filters at the top
5. **Get Tickets** - Click "GET TICKETS" on any event:
   - Enter your email
   - Check the opt-in box (required)
   - Click "Continue"
   - You'll be redirected to the event's original website

## What Happens Automatically

- **Scrapers run hourly** - Events are automatically updated every hour
- **Initial scrape** - Runs immediately when backend starts
- **Expired events** - Automatically marked as expired (won't show by default)

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"Playwright not found" errors:**
- Run `playwright install chromium`

**Port 8000 already in use:**
- Change port in `backend/.env`: `PORT=8001`
- Or stop the other application using port 8000

**Database errors:**
- Delete `backend/events.db` and restart (database will be recreated)

### Frontend Issues

**"Cannot connect to API" errors:**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/app/config.py`

**"npm install" fails:**
- Try `npm cache clean --force` then `npm install` again
- Make sure Node.js version is 18+

**Port 5173 already in use:**
- Vite will automatically use the next available port

### Scraping Issues

**No events appearing:**
- Check backend console for scraper logs
- Scrapers may take a few minutes on first run
- Some websites may block automated access (this is normal)

**Scrapers failing:**
- Check internet connection
- Some sites may have changed their HTML structure
- Check logs in backend console for specific errors

## Running Both Services

You need **two terminal windows**:

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
python -m app.main
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Stopping the Application

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal

## Next Steps

- Check the full [README.md](README.md) for detailed documentation
- Visit `http://localhost:8000/docs` for API documentation
- Customize settings in `backend/.env` file


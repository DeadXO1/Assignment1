# Sydney Events Scraper Application

A full-stack web application that automatically scrapes events from public event websites in Sydney, Australia, and displays them in a modern, responsive UI. Users can browse events, search and filter, and get tickets by providing their email address.

## Architecture Overview

The application consists of three main components:

1. **Scraping Layer**: Automated scrapers that collect event data from multiple sources (Eventbrite, Meetup, TimeOut Sydney)
2. **Backend API**: FastAPI server that stores events in SQLite and provides REST endpoints
3. **Frontend**: React application with Tailwind CSS for displaying events

### Data Flow

```
Scrapers (Hourly) → Database → API → Frontend → User
```

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: ORM for database operations
- **APScheduler**: Background job scheduler for automated scraping
- **Playwright**: Browser automation for JavaScript-heavy sites
- **BeautifulSoup4**: HTML parsing for static content
- **SQLite**: Lightweight database (easily migratable to PostgreSQL)

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework

## Project Structure

```
sydney-events-scraper/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models.py               # Database models (Event, Email)
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── events.py           # GET /api/events endpoint
│   │   │   └── emails.py           # POST /api/emails endpoint
│   │   ├── scrapers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base scraper class
│   │   │   ├── eventbrite.py       # Eventbrite scraper
│   │   │   ├── meetup.py           # Meetup scraper
│   │   │   └── timeout.py          # TimeOut Sydney scraper
│   │   └── scheduler.py             # APScheduler setup
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── components/
│   │   │   ├── EventCard.jsx       # Individual event card
│   │   │   ├── EventList.jsx       # List of events
│   │   │   ├── EmailModal.jsx     # Email capture modal
│   │   │   └── SearchFilter.jsx   # Search & filter
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   └── styles/
│   │       └── index.css           # Tailwind imports
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── .gitignore
└── README.md
```

## Database Schema

### Events Table
- `id` (Primary Key)
- `title` (String)
- `date_time` (DateTime)
- `location` (String)
- `description` (Text, nullable)
- `ticket_url` (String, unique)
- `image_url` (String, nullable)
- `source` (String: 'eventbrite', 'meetup', 'timeout')
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `expires_at` (DateTime, nullable)
- `click_count` (Integer, default: 0) - Analytics tracking

### Emails Table
- `id` (Primary Key)
- `email` (String, unique, indexed)
- `event_id` (Foreign Key → Events)
- `opt_in` (Boolean)
- `created_at` (DateTime)

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

6. Create environment file:
   ```bash
   copy .env.example .env  # Windows
   # or
   cp .env.example .env     # macOS/Linux
   ```

7. (Optional) Edit `.env` to customize settings:
   - `DATABASE_URL`: Database connection string
   - `CORS_ORIGINS`: Allowed frontend origins
   - `SCRAPER_DELAY_SECONDS`: Delay between requests (default: 3)
   - `CITY`: City to scrape events for (default: sydney)

8. Run the backend server:
   ```bash
   python -m app.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. (Optional) Create `.env` file to set API URL:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## How It Works

### Scraping

The application uses three scrapers to collect events:

1. **Eventbrite Scraper**: Scrapes from `eventbrite.com.au` for Sydney events
2. **Meetup Scraper**: Scrapes from `meetup.com` for Sydney meetups
3. **TimeOut Scraper**: Scrapes from `timeout.com/sydney/events`

Each scraper:
- Checks `robots.txt` before scraping
- Respects rate limiting (configurable delay between requests)
- Handles missing fields gracefully
- Deduplicates events by `ticket_url`
- Marks expired events automatically

### Automatic Updates

The application uses **APScheduler** to run all scrapers **hourly** in the background. The scheduler:
- Runs automatically when the backend starts
- Executes all scrapers sequentially
- Handles failures gracefully (one scraper failure doesn't stop others)
- Logs all scraping activities

### Email Capture Flow

1. User clicks "GET TICKETS" on an event card
2. Email modal appears requesting:
   - Email address (validated format)
   - Opt-in consent (required checkbox)
3. On submission:
   - Email is validated (format + opt-in requirement)
   - Email is stored in database
   - User is redirected to the original event website in a new tab

### API Endpoints

#### GET /api/events
Get paginated list of events with optional filters.

**Query Parameters:**
- `search` (string): Search in title, description, location
- `date_from` (YYYY-MM-DD): Filter events from this date
- `date_to` (YYYY-MM-DD): Filter events until this date
- `source` (string): Filter by source (eventbrite, meetup, timeout)
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20, max: 100)
- `include_expired` (bool): Include expired events (default: false)

**Response:**
```json
{
  "events": [...],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

#### GET /api/events/{id}
Get a single event by ID. Increments click count.

#### POST /api/emails
Capture user email with opt-in consent.

**Request Body:**
```json
{
  "email": "user@example.com",
  "event_id": 1,
  "opt_in": true
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "event_id": 1,
  "opt_in": true,
  "created_at": "2024-01-01T00:00:00"
}
```

## Ethical Scraping Considerations

This application follows ethical web scraping practices:

1. **Robots.txt Compliance**: All scrapers check and respect `robots.txt` files before scraping
2. **Rate Limiting**: Configurable delays (default: 3 seconds) between requests to avoid overwhelming servers
3. **User-Agent Identification**: Scrapers identify themselves with a clear user-agent string
4. **Public Data Only**: Only publicly available event data is scraped
5. **Minimal Data Storage**: Only necessary event fields are stored
6. **Error Handling**: Graceful error handling prevents excessive retries
7. **Terms of Service**: Users should review and comply with each website's Terms of Service

**Important**: Always review the Terms of Service of websites you scrape. Some sites may prohibit scraping or require API access.

## Features

### Core Features
- ✅ Automatic event scraping from multiple sources
- ✅ Hourly automatic updates
- ✅ Responsive, modern UI
- ✅ Email capture with opt-in consent
- ✅ Search and filter events
- ✅ Pagination
- ✅ Expired event handling

### Bonus Features
- ✅ Search by title/description/location
- ✅ Filter by date range
- ✅ Filter by source
- ✅ City configuration (via environment variable)
- ✅ Email confirmation message
- ✅ Click count analytics per event

## Development

### Running Tests

Currently, the application includes manual testing. To add automated tests:

**Backend:**
```bash
pytest backend/tests/
```

**Frontend:**
```bash
npm test
```

### Database Migration

The application uses SQLite by default. To migrate to PostgreSQL:

1. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/eventsdb
   ```

2. Install PostgreSQL adapter:
   ```bash
   pip install psycopg2-binary
   ```

3. Restart the application - tables will be created automatically.

## Troubleshooting

### Scrapers Not Running
- Check scheduler logs in the console
- Verify Playwright browsers are installed: `playwright install chromium`
- Check network connectivity

### Events Not Appearing
- Verify scrapers are running (check logs)
- Check database file exists: `backend/events.db`
- Verify CORS settings allow frontend origin

### Email Submission Fails
- Check backend API is running
- Verify email format is valid
- Ensure opt-in checkbox is checked
- Check browser console for errors

## License

This project is for educational purposes. Ensure compliance with website Terms of Service when scraping.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Notes

- Scrapers may need updates if website structures change
- Some sites may implement anti-scraping measures
- Consider using official APIs when available
- Database file (`events.db`) is created automatically on first run
- All scrapers handle missing fields gracefully (e.g., no image = placeholder)


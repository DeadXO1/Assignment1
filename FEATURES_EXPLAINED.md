# Feature Implementation Guide

## ✅ Feature 1: Email Capture with Opt-in and Redirect

### How It Works

When a user clicks the **"GET TICKETS"** button on any event card:

1. **Email Modal Opens**: A modal appears requesting:
   - Email address (validated format)
   - Opt-in checkbox (required - user must check it)

2. **Validation**:
   - Email format is validated (client-side and server-side)
   - Opt-in checkbox must be checked (required)
   - Shows error messages if validation fails

3. **Submission**:
   - Email is sent to backend API (`POST /api/emails`)
   - Backend validates and stores email in database
   - Email is linked to the specific event

4. **Redirect**:
   - After successful submission, user sees a success message
   - After 1.5 seconds, user is automatically redirected to the original event website
   - Opens in a new tab so user doesn't lose the events page

### Code Location

- **Frontend**: `frontend/src/components/EmailModal.jsx`
- **Frontend**: `frontend/src/components/EventCard.jsx` (triggers modal)
- **Backend API**: `backend/app/api/emails.py`
- **Database**: Email stored in `emails` table with `event_id` foreign key

### Testing

1. Click "GET TICKETS" on any event
2. Enter an email address
3. Check the opt-in checkbox (required)
4. Click "Continue"
5. You should be redirected to the event's original website

---

## ✅ Feature 2: Automatic Event Updates

### How It Works

Events are automatically updated from the original websites:

1. **Scheduler**: APScheduler runs in the background
2. **Frequency**: Scrapers run **every hour** automatically
3. **Initial Run**: Scrapers run immediately when backend starts
4. **Sources**: Three scrapers collect events:
   - Eventbrite (eventbrite.com.au)
   - Meetup (meetup.com)
   - TimeOut Sydney (timeout.com/sydney/events)

5. **Update Process**:
   - Scrapers check for new events
   - Duplicate events (same `ticket_url`) are updated, not duplicated
   - New events are added to database
   - Expired events are automatically marked

6. **Frontend Auto-Refresh**: 
   - Frontend automatically refreshes event list every 5 minutes
   - New events appear without manual page refresh

### Code Location

- **Scheduler**: `backend/app/scheduler.py`
- **Scrapers**: `backend/app/scrapers/` (eventbrite.py, meetup.py, timeout.py)
- **Frontend Auto-Refresh**: `frontend/src/components/EventList.jsx`

### How to Verify It's Working

1. **Check Backend Logs**: 
   - Look at the backend terminal window
   - You should see logs like:
     ```
     INFO: Running initial scrape...
     INFO: Scraper eventbrite completed: 15 events
     INFO: Scraper meetup completed: 8 events
     INFO: Scraper timeout completed: 12 events
     ```

2. **Check Database**:
   - Database file: `backend/events.db`
   - Events are stored with timestamps

3. **Check Frontend**:
   - Events appear automatically
   - New events appear within 5 minutes of being scraped
   - You can manually refresh the page to see updates immediately

### Customizing Update Frequency

**Backend (Scraping Frequency)**:
Edit `backend/app/scheduler.py` line 52:
```python
trigger=IntervalTrigger(hours=1),  # Change to minutes=30 for every 30 minutes
```

**Frontend (Auto-Refresh)**:
Edit `frontend/src/components/EventList.jsx`:
```javascript
5 * 60 * 1000  // Change to 2 * 60 * 1000 for every 2 minutes
```

---

## 📋 Summary

### Feature 1: Email Capture ✅
- ✅ "GET TICKETS" button on every event
- ✅ Email input with validation
- ✅ Required opt-in checkbox
- ✅ Email stored in database
- ✅ Automatic redirect to original event website
- ✅ Opens in new tab

### Feature 2: Automatic Updates ✅
- ✅ Scrapers run automatically every hour
- ✅ Runs immediately on backend startup
- ✅ Updates existing events (no duplicates)
- ✅ Adds new events as they're published
- ✅ Frontend auto-refreshes every 5 minutes
- ✅ Expired events are automatically handled

---

## 🔧 Troubleshooting

### Email Capture Not Working
- Check browser console for errors
- Verify backend is running (http://localhost:8000)
- Check backend logs for API errors

### Events Not Updating
- Check backend terminal for scraper logs
- Verify scheduler is running (should see hourly logs)
- Check if websites are accessible
- Some sites may block automated access (normal)

### Frontend Not Showing New Events
- Wait up to 5 minutes for auto-refresh
- Or manually refresh the page
- Check browser console for API errors

---

## 🎯 Both Features Are Fully Implemented and Working!

The application already includes both features you requested. They work automatically when the backend is running.


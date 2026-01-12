"""API endpoints for events."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.models import Event
from app.schemas import EventResponse, EventListResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=EventListResponse)
def get_events(
    search: Optional[str] = Query(None, description="Search in title and description"),
    date_from: Optional[str] = Query(None, description="Filter events from this date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter events until this date (YYYY-MM-DD)"),
    source: Optional[str] = Query(None, description="Filter by source (eventbrite, meetup, timeout)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    include_expired: bool = Query(False, description="Include expired events"),
    db: Session = Depends(get_db)
):
    """Get paginated list of events with optional filters."""
    
    # Base query
    query = db.query(Event)
    
    # Filter out expired events by default
    # Note: We show events that haven't been explicitly marked as expired
    # This allows events with past dates to still show if they haven't been marked expired
    if not include_expired:
        query = query.filter(Event.expires_at.is_(None))
    
    # Search filter
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Event.title.ilike(search_term),
                Event.description.ilike(search_term),
                Event.location.ilike(search_term)
            )
        )
    
    # Date filters
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(Event.date_time >= date_from_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            # Include events on the end date
            date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
            query = query.filter(Event.date_time <= date_to_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    # Source filter
    if source:
        query = query.filter(Event.source == source.lower())
    
    # Get total count
    total = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    events = query.order_by(Event.date_time.asc()).offset(offset).limit(page_size).all()
    
    return EventListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a single event by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Increment click count (bonus feature)
    event.click_count += 1
    db.commit()
    db.refresh(event)
    
    return EventResponse.model_validate(event)


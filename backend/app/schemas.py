"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    """Base event schema."""
    title: str
    date_time: datetime
    location: str
    description: Optional[str] = None
    ticket_url: str
    image_url: Optional[str] = None
    source: str


class EventCreate(EventBase):
    """Schema for creating an event."""
    pass


class EventResponse(EventBase):
    """Schema for event response."""
    id: int
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    click_count: int = 0
    
    class Config:
        from_attributes = True


class EmailCreate(BaseModel):
    """Schema for email capture."""
    email: EmailStr
    event_id: int
    opt_in: bool = Field(..., description="User must explicitly opt-in")


class EmailResponse(BaseModel):
    """Schema for email response."""
    id: int
    email: str
    event_id: int
    opt_in: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Schema for paginated event list."""
    events: list[EventResponse]
    total: int
    page: int
    page_size: int


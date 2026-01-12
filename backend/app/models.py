"""Database models for events and emails."""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Event(Base):
    """Event model representing scraped events."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    date_time = Column(DateTime, nullable=False, index=True)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    ticket_url = Column(String, unique=True, nullable=False, index=True)
    image_url = Column(String, nullable=True)
    source = Column(String, nullable=False, index=True)  # 'eventbrite', 'meetup', 'timeout'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)  # Bonus: analytics
    
    # Relationship
    emails = relationship("Email", back_populates="event")


class Email(Base):
    """Email model for storing user email captures."""
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    opt_in = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    event = relationship("Event", back_populates="emails")


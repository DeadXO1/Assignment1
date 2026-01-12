"""Base scraper class with common functionality."""
from abc import ABC, abstractmethod
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Event
from app.config import settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, db: Session, source_name: str, base_url: str):
        """
        Initialize base scraper.
        
        Args:
            db: Database session
            source_name: Name of the source (e.g., 'eventbrite')
            base_url: Base URL of the website to scrape
        """
        self.db = db
        self.source_name = source_name
        self.base_url = base_url
        self.delay = settings.scraper_delay_seconds
        self.timeout = settings.scraper_timeout_seconds
        self.user_agent = "SydneyEventsBot/1.0 (+https://github.com/sydney-events-scraper)"
        self.robot_parser = None
        self._check_robots_txt()
    
    def _check_robots_txt(self):
        """Check and parse robots.txt file."""
        try:
            robots_url = urljoin(self.base_url, "/robots.txt")
            self.robot_parser = RobotFileParser()
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            logger.info(f"Robots.txt checked for {self.base_url}")
        except Exception as e:
            logger.warning(f"Could not read robots.txt for {self.base_url}: {e}")
            # Create a permissive parser if robots.txt can't be read
            self.robot_parser = RobotFileParser()
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt.
        
        Args:
            url: URL to check
            
        Returns:
            True if allowed, False otherwise
        """
        if not self.robot_parser:
            return True
        
        try:
            return self.robot_parser.can_fetch(self.user_agent, url)
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True  # Default to allowing if check fails
    
    def rate_limit(self):
        """Apply rate limiting delay."""
        time.sleep(self.delay)
    
    def check_duplicate(self, ticket_url: str) -> Optional[Event]:
        """
        Check if event already exists in database.
        
        Args:
            ticket_url: Unique ticket URL to check
            
        Returns:
            Event if exists, None otherwise
        """
        return self.db.query(Event).filter(Event.ticket_url == ticket_url).first()
    
    def save_event(self, event_data: Dict) -> Event:
        """
        Save or update event in database.
        
        Args:
            event_data: Dictionary with event fields
            
        Returns:
            Saved Event object
        """
        # Check for duplicate
        existing_event = self.check_duplicate(event_data["ticket_url"])
        
        if existing_event:
            # Update existing event
            for key, value in event_data.items():
                if key != "ticket_url":  # Don't update unique identifier
                    setattr(existing_event, key, value)
            existing_event.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_event)
            logger.info(f"Updated event: {event_data['title']}")
            return existing_event
        else:
            # Create new event
            new_event = Event(**event_data)
            self.db.add(new_event)
            self.db.commit()
            self.db.refresh(new_event)
            logger.info(f"Created new event: {event_data['title']}")
            return new_event
    
    def mark_expired_events(self):
        """Mark events that have passed their date_time as expired.
        Only mark events that are at least 1 day old to avoid marking newly scraped events.
        """
        from datetime import timedelta
        now = datetime.utcnow()
        # Only mark events as expired if they're at least 1 day past their date
        # This prevents newly scraped events with incorrect dates from being marked expired
        cutoff_date = now - timedelta(days=1)
        expired_count = self.db.query(Event).filter(
            Event.source == self.source_name,
            Event.date_time < cutoff_date,
            Event.expires_at.is_(None)
        ).update({"expires_at": now})
        
        if expired_count > 0:
            self.db.commit()
            logger.info(f"Marked {expired_count} expired events from {self.source_name}")
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape events from the source.
        
        Returns:
            List of event dictionaries
        """
        pass
    
    def run(self) -> int:
        """
        Run the scraper and save events to database.
        
        Returns:
            Number of events scraped
        """
        try:
            logger.info(f"Starting scraper for {self.source_name}")
            
            # Mark expired events first
            self.mark_expired_events()
            
            # Scrape events
            events = self.scrape()
            
            # Save events
            saved_count = 0
            for event_data in events:
                try:
                    # Ensure source is set
                    event_data["source"] = self.source_name
                    self.save_event(event_data)
                    saved_count += 1
                    self.rate_limit()  # Rate limit between saves
                except Exception as e:
                    logger.error(f"Error saving event {event_data.get('title', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Scraper {self.source_name} completed: {saved_count} events saved")
            return saved_count
            
        except Exception as e:
            logger.error(f"Error in scraper {self.source_name}: {e}", exc_info=True)
            return 0


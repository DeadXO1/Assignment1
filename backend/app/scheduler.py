"""Background scheduler for running scrapers."""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.scrapers.eventbrite import EventbriteScraper
from app.scrapers.meetup import MeetupScraper
from app.scrapers.timeout import TimeOutScraper

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def run_all_scrapers():
    """Run all scrapers and handle errors gracefully."""
    db: Session = SessionLocal()
    
    try:
        scrapers = [
            EventbriteScraper(db),
            MeetupScraper(db),
            TimeOutScraper(db)
        ]
        
        for scraper in scrapers:
            try:
                count = scraper.run()
                logger.info(f"Scraper {scraper.source_name} completed: {count} events")
            except Exception as e:
                logger.error(f"Scraper {scraper.source_name} failed: {e}", exc_info=True)
                # Continue with other scrapers even if one fails
                continue
    
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler."""
    if scheduler.running:
        logger.warning("Scheduler is already running")
        return
    
    # Initialize database
    init_db()
    
    # Schedule scrapers to run hourly
    scheduler.add_job(
        func=run_all_scrapers,
        trigger=IntervalTrigger(hours=1),
        id="scrape_events",
        name="Scrape events from all sources",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started - scrapers will run hourly")
    
    # Run once immediately on startup
    logger.info("Running initial scrape...")
    run_all_scrapers()


def stop_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


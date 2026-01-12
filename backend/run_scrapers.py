"""Manual script to run scrapers immediately."""
import logging
from app.database import SessionLocal, init_db
from app.scrapers.eventbrite import EventbriteScraper
from app.scrapers.meetup import MeetupScraper
from app.scrapers.timeout import TimeOutScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    """Run all scrapers manually."""
    logger.info("=" * 50)
    logger.info("Starting manual scraper run...")
    logger.info("=" * 50)
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        scrapers = [
            EventbriteScraper(db),
            MeetupScraper(db),
            TimeOutScraper(db)
        ]
        
        total_events = 0
        
        for scraper in scrapers:
            try:
                logger.info(f"\n{'='*50}")
                logger.info(f"Running {scraper.source_name} scraper...")
                logger.info(f"{'='*50}")
                count = scraper.run()
                total_events += count
                logger.info(f"✓ {scraper.source_name} completed: {count} events saved")
            except Exception as e:
                logger.error(f"✗ {scraper.source_name} failed: {e}", exc_info=True)
                continue
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Scraping complete! Total events saved: {total_events}")
        logger.info(f"{'='*50}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()


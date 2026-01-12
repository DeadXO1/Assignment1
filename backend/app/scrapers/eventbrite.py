"""Eventbrite scraper for Sydney events."""
import logging
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from playwright.async_api import async_playwright, Browser, Page
import asyncio
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.config import settings

logger = logging.getLogger(__name__)


class EventbriteScraper(BaseScraper):
    """Scraper for Eventbrite Sydney events."""
    
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            source_name="eventbrite",
            base_url="https://www.eventbrite.com.au"
        )
        self.city = settings.city
        self.browser: Browser = None
        self.page: Page = None
        self.playwright = None
    
    async def _init_browser(self):
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.set_extra_http_headers({
            "User-Agent": self.user_agent
        })
    
    async def _close_browser(self):
        """Close Playwright browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def _scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page of events."""
        events = []
        
        try:
            if not self.can_fetch(url):
                logger.warning(f"Robots.txt disallows: {url}")
                return events
            
            await self.page.goto(url, wait_until="networkidle", timeout=self.timeout * 1000)
            await asyncio.sleep(2)  # Wait for dynamic content
            
            # Get page content
            content = await self.page.content()
            soup = BeautifulSoup(content, "lxml")
            
            # Find event cards (Eventbrite structure may vary, this is a general approach)
            event_cards = soup.find_all("div", class_=lambda x: x and "event-card" in x.lower()) or \
                         soup.find_all("article") or \
                         soup.find_all("div", {"data-testid": lambda x: x and "event" in x.lower()})
            
            if not event_cards:
                # Try alternative selectors
                event_cards = soup.select("[class*='event']")[:20]  # Limit to prevent too many
            
            for card in event_cards[:50]:  # Limit events per page
                try:
                    event_data = self._extract_event_data(card, soup)
                    if event_data and event_data.get("ticket_url"):
                        events.append(event_data)
                except Exception as e:
                    logger.debug(f"Error extracting event from card: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")
        
        return events
    
    def _extract_event_data(self, card, soup) -> Dict:
        """Extract event data from a card element."""
        event_data = {}
        
        try:
            # Title
            title_elem = card.find("h2") or card.find("h3") or card.find("a", class_=lambda x: x and "title" in x.lower() if x else False)
            if not title_elem:
                title_elem = card.find("a", href=True)
            event_data["title"] = title_elem.get_text(strip=True) if title_elem else "Untitled Event"
            
            # Ticket URL
            link_elem = card.find("a", href=True)
            if link_elem:
                href = link_elem.get("href", "")
                if href.startswith("/"):
                    event_data["ticket_url"] = f"{self.base_url}{href}"
                elif href.startswith("http"):
                    event_data["ticket_url"] = href
                else:
                    event_data["ticket_url"] = f"{self.base_url}/{href}"
            else:
                return None  # Skip if no URL
            
            # Date and time (try multiple selectors)
            date_elem = card.find("time") or card.find("div", class_=lambda x: x and "date" in x.lower() if x else False)
            if date_elem:
                date_str = date_elem.get_text(strip=True)
                # Try to parse date (simplified - may need more robust parsing)
                event_data["date_time"] = self._parse_date(date_str)
            else:
                event_data["date_time"] = datetime.utcnow()  # Default to now if not found
            
            # Location
            location_elem = card.find("div", class_=lambda x: x and "location" in x.lower() if x else False) or \
                           card.find("span", class_=lambda x: x and "location" in x.lower() if x else False)
            event_data["location"] = location_elem.get_text(strip=True) if location_elem else f"{self.city.capitalize()}, Australia"
            
            # Description
            desc_elem = card.find("p") or card.find("div", class_=lambda x: x and "description" in x.lower() if x else False)
            event_data["description"] = desc_elem.get_text(strip=True)[:500] if desc_elem else None  # Limit description length
            
            # Image
            img_elem = card.find("img")
            if img_elem:
                img_src = img_elem.get("src") or img_elem.get("data-src")
                if img_src:
                    if img_src.startswith("/"):
                        event_data["image_url"] = f"{self.base_url}{img_src}"
                    elif img_src.startswith("http"):
                        event_data["image_url"] = img_src
                    else:
                        event_data["image_url"] = None
                else:
                    event_data["image_url"] = None
            else:
                event_data["image_url"] = None
            
        except Exception as e:
            logger.debug(f"Error extracting event data: {e}")
            return None
        
        return event_data
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime object."""
        # This is a simplified parser - in production, use dateutil or similar
        try:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%d %b %Y", "%d/%m/%Y", "%B %d, %Y"]:
                try:
                    return datetime.strptime(date_str[:20], fmt)
                except:
                    continue
        except:
            pass
        
        # Default to 7 days from now if parsing fails (so event shows up)
        from datetime import timedelta
        return datetime.utcnow() + timedelta(days=7)
    
    async def _scrape_async(self) -> List[Dict]:
        """Async scraping method."""
        all_events = []
        
        try:
            await self._init_browser()
            
            # Eventbrite Sydney events URL
            search_url = f"{self.base_url}/d/australia--sydney/events/"
            
            # Scrape first few pages
            for page_num in range(1, 4):  # Scrape first 3 pages
                if page_num == 1:
                    url = search_url
                else:
                    url = f"{search_url}?page={page_num}"
                
                events = await self._scrape_page(url)
                all_events.extend(events)
                
                if len(events) == 0:
                    break  # No more events
                
                await asyncio.sleep(self.delay)
            
        except Exception as e:
            logger.error(f"Error in async scraping: {e}")
        finally:
            await self._close_browser()
        
        return all_events
    
    def scrape(self) -> List[Dict]:
        """Synchronous interface for scraping."""
        return asyncio.run(self._scrape_async())


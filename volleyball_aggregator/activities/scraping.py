import json
from typing import Dict, Any, List
from temporalio import activity
import asyncio
from ..models.team import Team
from ..scrapers.base import BaseScraper
from ..config import settings
import logging

logger = logging.getLogger(__name__)

@activity.defn
async def scrape_source(source: Dict[str, str]) -> List[Dict[str, Any]]:
    """Activity to scrape a specific source (NCAA D1, D3, or Canadian)."""
    logger.info(f"Starting scrape for {source['name']}")
    
    # Import the appropriate scraper based on the division
    scraper_class = _get_scraper_class(source['division'])
    if not scraper_class:
        raise ValueError(f"No scraper implemented for division: {source['division']}")

    # Initialize and run the scraper
    async with scraper_class(source['base_url']) as scraper:
        teams = await scraper.scrape_all()
        # Add a delay between batches as configured
        await asyncio.sleep(settings.SCRAPE_DELAY_SECONDS)
        return [team.model_dump() for team in teams]

@activity.defn
async def store_results(results: List[Dict[str, Any]]) -> None:
    """Activity to store the scraped results."""
    timestamp = activity.info().started_at.strftime("%Y%m%d_%H%M%S")
    filename = settings.output_path / f"volleyball_teams_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Stored {len(results)} teams in {filename}")
    except Exception as e:
        logger.error(f"Error storing results: {str(e)}")
        raise

def _get_scraper_class(division: str) -> type[BaseScraper]:
    """Helper function to get the appropriate scraper class based on division."""
    # This would be replaced with actual scraper implementations
    from ..scrapers.ncaa import NCAADivisionScraper
    from ..scrapers.canadian import CanadianScraper
    
    scrapers = {
        "NCAA_D1": NCAADivisionScraper,
        "NCAA_D3": NCAADivisionScraper,
        "CANADIAN": CanadianScraper
    }
    
    return scrapers.get(division) 
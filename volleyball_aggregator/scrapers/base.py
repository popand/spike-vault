from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.team import Team
import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    @abstractmethod
    async def get_team_list(self) -> List[str]:
        """Get a list of team URLs to scrape."""
        pass

    @abstractmethod
    async def scrape_team(self, team_url: str) -> Team:
        """Scrape a single team's information."""
        pass

    async def scrape_all(self) -> List[Team]:
        """Scrape all teams from this source."""
        teams = []
        try:
            team_urls = await self.get_team_list()
            for url in team_urls:
                try:
                    team = await self.scrape_team(url)
                    teams.append(team)
                except Exception as e:
                    logger.error(f"Error scraping team {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting team list: {str(e)}")
        return teams

    async def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Helper method to fetch and parse a page."""
        if not self._session:
            raise RuntimeError("Scraper must be used as an async context manager")
        
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    return BeautifulSoup(html, 'html.parser')
                else:
                    logger.error(f"Failed to fetch {url}: Status {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None 
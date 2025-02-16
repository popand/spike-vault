from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
import logging
from .base import BaseScraper
from ..models.team import Team, Coach, Player

logger = logging.getLogger(__name__)

class CanadianScraper(BaseScraper):
    WATERLOO_URL = "https://athletics.uwaterloo.ca/sports/womens-volleyball/roster"
    
    async def get_team_list(self) -> List[str]:
        """Get a list of Canadian university team URLs."""
        # For now, we'll just return Waterloo's URL
        return [self.WATERLOO_URL]

    async def scrape_team(self, team_url: str) -> Team:
        """Scrape a Canadian university team."""
        soup = await self._fetch_page(team_url)
        if not soup:
            raise ValueError(f"Failed to fetch team page: {team_url}")

        if "waterloo" in team_url.lower():
            return await self._scrape_waterloo(soup, team_url)
        
        raise ValueError(f"Unsupported Canadian university URL: {team_url}")

    async def _scrape_waterloo(self, soup: BeautifulSoup, url: str) -> Team:
        """Scrape Waterloo Warriors women's volleyball team."""
        # Extract players
        players = []
        roster_section = soup.find('section', {'class': 'sidearm-roster-players'})
        if roster_section:
            for player_div in roster_section.find_all('li', {'class': 'sidearm-roster-player'}):
                try:
                    player = self._extract_waterloo_player(player_div)
                    if player:
                        players.append(player)
                except Exception as e:
                    logger.error(f"Error extracting player: {str(e)}")

        # Extract coaches
        coaches = []
        coaches_section = soup.find('div', text='Women\'s Volleyball Coaching Staff')
        if coaches_section:
            coach_divs = coaches_section.find_next('div').find_all('div', {'class': 'sidearm-roster-coach'})
            for coach_div in coach_divs:
                try:
                    coach = self._extract_waterloo_coach(coach_div)
                    if coach:
                        coaches.append(coach)
                except Exception as e:
                    logger.error(f"Error extracting coach: {str(e)}")

        return Team(
            school_name="University of Waterloo",
            division="CANADIAN",
            conference="OUA",
            mascot="Warriors",
            location="Waterloo, ON",
            head_coach=coaches[0] if coaches else None,
            assistant_coaches=coaches[1:] if len(coaches) > 1 else [],
            players=players,
            website_url=url
        )

    def _extract_waterloo_player(self, player_div: BeautifulSoup) -> Optional[Player]:
        """Extract player information from Waterloo's roster page."""
        try:
            # Basic info
            name = player_div.find('h3').text.strip()
            
            # Details
            details = player_div.find_all('span', {'class': 'sidearm-roster-player-details'})
            position = ""
            number = ""
            height = ""
            year = ""
            hometown = ""
            
            for detail in details:
                text = detail.text.strip()
                if "Position:" in text:
                    position = text.replace("Position:", "").strip()
                elif "Height:" in text:
                    height = text.replace("Height:", "").strip()
                elif "Year:" in text:
                    year = text.replace("Year:", "").strip()
                elif "Hometown:" in text:
                    hometown = text.replace("Hometown:", "").strip()
                elif text.isdigit():
                    number = text

            return Player(
                name=name,
                number=number,
                position=position,
                year=year,
                hometown=hometown,
                height=height
            )
        except Exception as e:
            logger.error(f"Error parsing player: {str(e)}")
            return None

    def _extract_waterloo_coach(self, coach_div: BeautifulSoup) -> Optional[Coach]:
        """Extract coach information from Waterloo's roster page."""
        try:
            name_elem = coach_div.find('h3')
            title_elem = coach_div.find('div', {'class': 'sidearm-roster-coach-title'})
            
            if name_elem and title_elem:
                return Coach(
                    name=name_elem.text.strip(),
                    title=title_elem.text.strip()
                )
            return None
        except Exception as e:
            logger.error(f"Error parsing coach: {str(e)}")
            return None 
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class Player(BaseModel):
    name: str
    number: Optional[str] = None
    position: Optional[str] = None
    year: Optional[str] = None
    hometown: Optional[str] = None
    height: Optional[str] = None

class Coach(BaseModel):
    name: str
    title: str
    years_at_school: Optional[int] = None
    career_record: Optional[str] = None

class Team(BaseModel):
    school_name: str
    division: str  # "NCAA_D1", "NCAA_D3", "CANADIAN"
    conference: Optional[str] = None
    mascot: Optional[str] = None
    location: Optional[str] = None
    head_coach: Optional[Coach] = None
    assistant_coaches: List[Coach] = Field(default_factory=list)
    players: List[Player] = Field(default_factory=list)
    website_url: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "school_name": "Example University",
                "division": "NCAA_D1",
                "conference": "Example Conference",
                "mascot": "Eagles",
                "location": "City, State",
                "head_coach": {
                    "name": "Jane Doe",
                    "title": "Head Coach",
                    "years_at_school": 5,
                    "career_record": "120-45"
                }
            }
        } 
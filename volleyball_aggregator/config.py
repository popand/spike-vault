import os
from pathlib import Path
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    # Temporal Server Configuration
    TEMPORAL_HOST: str = "viaduct.proxy.rlwy.net"
    TEMPORAL_PORT: int = 46280
    
    # Derived Temporal URL
    @property
    def temporal_url(self) -> str:
        return f"{self.TEMPORAL_HOST}:{self.TEMPORAL_PORT}"
    
    # Scraping Configuration
    SCRAPE_BATCH_SIZE: int = 10
    SCRAPE_DELAY_SECONDS: int = 5
    
    # Storage Configuration
    OUTPUT_DIR: str = "data"
    
    # OpenAI Configuration
    OPENAI_API_KEY: SecretStr
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_API_KEY: SecretStr
    GOOGLE_SHEET_ID: str
    
    @property
    def output_path(self) -> Path:
        path = Path(self.OUTPUT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings() 
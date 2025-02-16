# Volleyball Teams Data Aggregator

A robust data aggregation system that collects and processes information about volleyball teams from NCAA Division I, Division III, and Canadian universities. The system uses Temporal workflows for reliable task orchestration and features concurrent scraping capabilities.

## 🌟 Features

- **Multi-Source Data Collection**
  - NCAA Division I volleyball teams
  - NCAA Division III volleyball teams
  - Canadian university volleyball teams

- **Robust Workflow Orchestration**
  - Temporal-based workflow management
  - Concurrent scraping with rate limiting
  - Automatic retries and error handling
  - Configurable execution parameters

- **Data Processing**
  - Standardized data models
  - Automated data normalization
  - JSON-based storage with timestamps
  - Extensible storage backend

## 🏗 Architecture

### Workflow Structure
```
Main Aggregator Workflow
├── NCAA D1 Child Workflow
│   └── Scraping Activities
├── NCAA D3 Child Workflow
│   └── Scraping Activities
└── Canadian Universities Child Workflow
    └── Scraping Activities
```

### Component Overview
- **Workflows**: Orchestrate the scraping process
  - `DataAggregatorWorkflow`: Main workflow coordinator
  - `ScrapeSourceWorkflow`: Individual source handler

- **Activities**: Perform actual work
  - `scrape_source`: Handles data collection
  - `store_results`: Manages data persistence

- **Models**: Define data structures
  - `Team`: Core team information
  - `Player`: Player details
  - `Coach`: Coaching staff information

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Temporal server
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/popand/spike-vault.git
cd spike-vault
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

### Configuration

The system can be configured through environment variables:

```env
# Temporal Server Configuration
TEMPORAL_HOST=viaduct.proxy.rlwy.net
TEMPORAL_PORT=46280

# Scraping Configuration
SCRAPE_BATCH_SIZE=10
SCRAPE_DELAY_SECONDS=5

# Storage Configuration
OUTPUT_DIR=data
```

### Usage

1. Start the Temporal worker:
```bash
python -m volleyball_aggregator.worker
```

2. Run the aggregator workflow:
```bash
python -m volleyball_aggregator.run
```

## 📁 Project Structure

```
volleyball_aggregator/
├── activities/
│   └── scraping.py      # Scraping activities
├── models/
│   └── team.py          # Data models
├── scrapers/
│   ├── base.py          # Base scraper class
│   └── ncaa.py          # NCAA implementation
├── workflows/
│   └── aggregator.py    # Workflow definitions
├── config.py            # Configuration management
├── worker.py            # Temporal worker
└── run.py              # Entry point
```

## 🔧 Development

### Adding New Data Sources

1. Create a new scraper class:
```python
from .base import BaseScraper

class NewSourceScraper(BaseScraper):
    async def get_team_list(self) -> List[str]:
        # Implement team list retrieval
        pass

    async def scrape_team(self, team_url: str) -> Team:
        # Implement team data scraping
        pass
```

2. Register the scraper in `activities/scraping.py`:
```python
scrapers = {
    "NEW_SOURCE": NewSourceScraper,
    # ... existing scrapers
}
```

### Error Handling

The system implements multiple layers of error handling:
- Activity-level retries with exponential backoff
- Workflow-level error recovery
- Logging for debugging and monitoring

## 📊 Data Format

Example team data structure:
```json
{
  "school_name": "Example University",
  "division": "NCAA_D1",
  "conference": "Example Conference",
  "mascot": "Eagles",
  "head_coach": {
    "name": "Jane Doe",
    "title": "Head Coach",
    "years_at_school": 5
  },
  "players": [
    {
      "name": "Player Name",
      "number": "10",
      "position": "Outside Hitter"
    }
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Temporal](https://temporal.io/) for workflow orchestration
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation 
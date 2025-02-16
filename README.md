# Volleyball Teams Data Aggregator

A data aggregation system that scrapes information about volleyball teams from NCAA Division I, Division III, and Canadian universities using Temporal workflows for orchestration.

## Features

- Concurrent scraping of multiple data sources
- Scheduled data collection
- Robust error handling and retries
- Data normalization across different sources
- Temporal workflow orchestration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Temporal server:
Make sure you have a Temporal server running. You can use the Temporal CLI or Docker:
```bash
temporal server start-dev
```

3. Configure environment variables:
Create a `.env` file with necessary configurations (see `.env.example`).

## Usage

1. Start the Temporal worker:
```bash
python -m volleyball_aggregator.worker
```

2. Run the main workflow:
```bash
python -m volleyball_aggregator.run
```

## Project Structure

- `volleyball_aggregator/` - Main package directory
  - `workflows/` - Temporal workflow definitions
  - `activities/` - Temporal activity implementations
  - `models/` - Data models and schemas
  - `scrapers/` - Web scraping implementations
  - `worker.py` - Temporal worker setup
  - `run.py` - Workflow execution entry point

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License 
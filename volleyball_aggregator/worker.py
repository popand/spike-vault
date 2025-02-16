import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from .workflows.aggregator import DataAggregatorWorkflow, ScrapeSourceWorkflow
from .activities.scraping import scrape_source, store_results
from .config import settings

async def run_worker():
    # Initialize the client with configured server
    client = await Client.connect(settings.temporal_url)

    # Run the worker
    worker = Worker(
        client,
        task_queue="volleyball-scraper",
        workflows=[DataAggregatorWorkflow, ScrapeSourceWorkflow],
        activities=[scrape_source, store_results]
    )

    logging.info(f"Starting worker... Connected to Temporal server at {settings.temporal_url}")
    await worker.run()

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(run_worker())

if __name__ == "__main__":
    main() 
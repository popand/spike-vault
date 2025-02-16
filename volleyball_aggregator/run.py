import asyncio
import logging
from datetime import timedelta
from temporalio.client import Client
from .workflows.aggregator import DataAggregatorWorkflow
from .config import settings

async def main():
    # Initialize the client with configured server
    client = await Client.connect(settings.temporal_url)

    # Start the workflow
    handle = await client.start_workflow(
        DataAggregatorWorkflow.run,
        id="volleyball-scraper",
        task_queue="volleyball-scraper",
        execution_timeout=timedelta(hours=2)
    )

    logging.info(f"Started workflow with ID {handle.id} on server {settings.temporal_url}")
    
    # Wait for the result
    result = await handle.result()
    logging.info(f"Workflow completed with {len(result)} teams scraped")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main()) 
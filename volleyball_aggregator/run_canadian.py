import asyncio
from datetime import timedelta
from temporalio.client import Client
from temporalio.common import RetryPolicy
from .config import settings

async def main():
    # Create client connected to server
    client = await Client.connect(settings.temporal_url)

    # Start a workflow
    source = {
        "name": "Canadian Universities",
        "division": "CANADIAN",
        "base_url": "https://usports.ca/en/sports/volleyball/f"
    }

    # Execute the workflow
    handle = await client.start_workflow(
        "ScrapeSourceWorkflow",
        source,
        id="scrape-canadian",
        task_queue="volleyball-tasks",
        retry_policy=RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(minutes=10),
            maximum_attempts=3,
            non_retryable_error_types=["ValueError"]
        )
    )

    print(f"Started workflow with ID: {handle.id}")
    
    # Wait for the workflow to complete
    result = await handle.result()
    print("Workflow completed!")
    print(f"Number of teams scraped: {len(result)}")
    return result

if __name__ == "__main__":
    asyncio.run(main()) 
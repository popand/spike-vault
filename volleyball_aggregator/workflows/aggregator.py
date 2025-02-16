from datetime import timedelta
from typing import List, Dict, Any
import asyncio
from temporalio import workflow
from temporalio.common import RetryPolicy
from ..models.team import Team

@workflow.defn
class DataAggregatorWorkflow:
    @workflow.run
    async def run(self) -> List[Dict[str, Any]]:
        sources = [
            {
                "name": "NCAA Division I",
                "division": "NCAA_D1",
                "base_url": "https://www.ncaa.com/schools"
            },
            {
                "name": "NCAA Division III",
                "division": "NCAA_D3",
                "base_url": "https://www.ncaa.com/schools"
            },
            {
                "name": "Canadian Universities",
                "division": "CANADIAN",
                "base_url": "https://usports.ca/en/sports/volleyball/f"
            }
        ]

        # Create child workflows for each source
        results = []
        for source in sources:
            try:
                result = await workflow.execute_child_workflow(
                    "ScrapeSourceWorkflow",
                    source,
                    id=f"scrape-{source['division'].lower()}",
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=1),
                        maximum_interval=timedelta(minutes=10),
                        maximum_attempts=3,
                        non_retryable_error_types=["ValueError"]
                    )
                )
                results.extend(result)
            except Exception as e:
                workflow.logger.error(f"Error in child workflow for {source['name']}: {str(e)}")

        # Store results
        if results:
            await workflow.execute_activity(
                "store_results",
                results,
                start_to_close_timeout=timedelta(minutes=5)
            )

        return results

@workflow.defn
class ScrapeSourceWorkflow:
    @workflow.run
    async def run(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        # Add a small delay to prevent overwhelming the sources
        await asyncio.sleep(5)

        # Execute the scraping activity
        teams = await workflow.execute_activity(
            "scrape_source",
            source,
            start_to_close_timeout=timedelta(minutes=30),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(minutes=10),
                maximum_attempts=3
            )
        )

        return teams 
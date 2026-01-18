"""YouTube utility functions."""

from apify_client import ApifyClient

from .schemas import YouTubeResponse


def run_actor(client: ApifyClient, actor_id: str, actor_input: dict) -> YouTubeResponse:
    """Execute an Apify actor and return results."""
    run = client.actor(actor_id).call(run_input=actor_input)

    dataset_id = run.get("defaultDatasetId")
    items = []

    if dataset_id:
        dataset_items = client.dataset(dataset_id).list_items()
        items = dataset_items.items

    return YouTubeResponse(
        success=True,
        data=items,
        total_results=len(items),
        run_id=run.get("id"),
    )

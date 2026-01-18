"""TikTok hashtag scraping service."""

from apify_client import ApifyClient

from .constants import TIKTOK_ACTOR_ID, TIKTOK_DEFAULT_RESULTS
from .schemas import TikTokHashtagRequest, TikTokResponse


def build_hashtag_input(request: TikTokHashtagRequest) -> dict:
    """Build the input payload for hashtag scraping."""
    return {
        "hashtags": [request.hashtag],
        "resultsPerPage": request.limit,
    }


async def scrape_hashtag(
    client: ApifyClient,
    hashtag: str,
    limit: int = TIKTOK_DEFAULT_RESULTS,
) -> TikTokResponse:
    """
    Scrape TikTok videos by hashtag.

    Args:
        client: Apify client instance
        hashtag: Hashtag to scrape (without #)
        limit: Maximum number of results

    Returns:
        TikTokResponse with videos
    """
    request = TikTokHashtagRequest(hashtag=hashtag, limit=limit)
    actor_input = build_hashtag_input(request)

    run = client.actor(TIKTOK_ACTOR_ID).call(run_input=actor_input)

    dataset_id = run.get("defaultDatasetId")
    items = []

    if dataset_id:
        dataset_items = client.dataset(dataset_id).list_items()
        items = dataset_items.items

    return TikTokResponse(
        success=True,
        data=items,
        total_results=len(items),
        run_id=run.get("id"),
    )

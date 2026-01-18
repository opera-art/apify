"""TikTok profile scraping service."""

from apify_client import ApifyClient

from .constants import TIKTOK_ACTOR_ID, TIKTOK_DEFAULT_RESULTS
from .schemas import TikTokProfileRequest, TikTokResponse


def build_profile_input(request: TikTokProfileRequest) -> dict:
    """Build the input payload for profile scraping."""
    return {
        "profiles": [request.username],
        "resultsPerPage": request.limit,
    }


async def scrape_profile(
    client: ApifyClient,
    username: str,
    limit: int = TIKTOK_DEFAULT_RESULTS,
) -> TikTokResponse:
    """
    Scrape TikTok profile and videos.

    Args:
        client: Apify client instance
        username: TikTok username
        limit: Maximum number of videos

    Returns:
        TikTokResponse with profile and videos
    """
    request = TikTokProfileRequest(username=username, limit=limit)
    actor_input = build_profile_input(request)

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

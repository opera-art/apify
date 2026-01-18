"""TikTok video details service."""

from apify_client import ApifyClient

from .constants import TIKTOK_ACTOR_ID
from .schemas import TikTokVideoRequest, TikTokResponse


def build_video_input(request: TikTokVideoRequest) -> dict:
    """Build the input payload for video details."""
    return {
        "postURLs": [request.url],
        "resultsPerPage": 1,
    }


async def get_video(
    client: ApifyClient,
    url: str,
) -> TikTokResponse:
    """
    Get TikTok video details.

    Args:
        client: Apify client instance
        url: TikTok video URL

    Returns:
        TikTokResponse with video details
    """
    request = TikTokVideoRequest(url=url)
    actor_input = build_video_input(request)

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

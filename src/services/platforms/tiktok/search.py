"""TikTok search service."""

from apify_client import ApifyClient

from .constants import TIKTOK_ACTOR_ID, TIKTOK_DEFAULT_RESULTS
from .types import TikTokSearchType
from .schemas import TikTokSearchRequest, TikTokResponse


def build_search_input(request: TikTokSearchRequest) -> dict:
    """Build the input payload for search."""
    return {
        "searchQueries": [request.query],
        "resultsPerPage": request.limit,
        "searchSection": request.search_type.value,
    }


async def search(
    client: ApifyClient,
    query: str,
    search_type: TikTokSearchType = TikTokSearchType.TOP,
    limit: int = TIKTOK_DEFAULT_RESULTS,
) -> TikTokResponse:
    """
    Search TikTok.

    Args:
        client: Apify client instance
        query: Search query
        search_type: Type of search (video, user, top)
        limit: Maximum number of results

    Returns:
        TikTokResponse with search results
    """
    request = TikTokSearchRequest(
        query=query,
        search_type=search_type,
        limit=limit,
    )
    actor_input = build_search_input(request)

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

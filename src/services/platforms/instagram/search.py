"""Instagram search service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_ACTOR_ID
from .types import InstagramSearchType
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramSearchRequest(BaseModel):
    """Request to search Instagram."""

    query: str = Field(
        ...,
        description="Search query",
    )
    search_type: InstagramSearchType = Field(
        default=InstagramSearchType.USER,
        alias="searchType",
        description="Type of search: user, hashtag, or place",
    )
    results_limit: int = Field(
        default=10,
        alias="resultsLimit",
        ge=1,
        le=100,
        description="Maximum search results",
    )

    class Config:
        populate_by_name = True


def build_search_input(request: InstagramSearchRequest) -> dict:
    """Build the input payload for search."""
    return {
        "search": request.query,
        "searchType": request.search_type.value,
        "searchLimit": request.results_limit,
        "resultsType": "details",
        "proxy": get_default_proxy(),
    }


def search(
    client: ApifyClient,
    request: InstagramSearchRequest,
) -> InstagramResponse:
    """
    Search Instagram for users, hashtags, or places.

    Returns: search results based on type.
    """
    actor_input = build_search_input(request)
    return run_actor(client, INSTAGRAM_ACTOR_ID, actor_input)


def search_users(
    client: ApifyClient,
    query: str,
    limit: int = 10,
) -> InstagramResponse:
    """Search for Instagram users."""
    request = InstagramSearchRequest(
        query=query,
        search_type=InstagramSearchType.USER,
        results_limit=limit,
    )
    return search(client, request)


def search_hashtags(
    client: ApifyClient,
    query: str,
    limit: int = 10,
) -> InstagramResponse:
    """Search for Instagram hashtags."""
    request = InstagramSearchRequest(
        query=query,
        search_type=InstagramSearchType.HASHTAG,
        results_limit=limit,
    )
    return search(client, request)


def search_places(
    client: ApifyClient,
    query: str,
    limit: int = 10,
) -> InstagramResponse:
    """Search for Instagram places/locations."""
    request = InstagramSearchRequest(
        query=query,
        search_type=InstagramSearchType.PLACE,
        results_limit=limit,
    )
    return search(client, request)

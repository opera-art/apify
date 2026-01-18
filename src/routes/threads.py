"""Threads API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.threads import (
    ThreadsResponse,
    scrape_profile,
    scrape_hashtag,
    search,
    get_thread,
)

router = APIRouter(prefix="/threads", tags=["Threads"])


@router.get(
    "/profile/{username}",
    response_model=ThreadsResponse,
    summary="Scrape profile threads",
)
async def get_profile_threads(
    username: str,
    limit: int = Query(default=20, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> ThreadsResponse:
    """Get threads from a user profile."""
    try:
        return await scrape_profile(client, username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/hashtag/{hashtag}",
    response_model=ThreadsResponse,
    summary="Scrape by hashtag",
)
async def get_hashtag_threads(
    hashtag: str,
    limit: int = Query(default=20, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> ThreadsResponse:
    """Get threads by hashtag."""
    try:
        return await scrape_hashtag(client, hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=ThreadsResponse,
    summary="Search Threads",
)
async def search_threads(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> ThreadsResponse:
    """Search Threads."""
    try:
        return await search(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/thread",
    response_model=ThreadsResponse,
    summary="Get thread details",
)
async def get_thread_details(
    url: str = Query(..., description="Threads post URL"),
    include_replies: bool = Query(default=False, alias="includeReplies"),
    client: ApifyClient = Depends(get_apify_client),
) -> ThreadsResponse:
    """Get thread details by URL."""
    try:
        return await get_thread(client, url, include_replies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""Threads API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.threads import (
    ThreadsService,
    ThreadsScrapeRequest,
    ThreadsScrapeResponse,
)

router = APIRouter(prefix="/threads", tags=["Threads"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> ThreadsService:
    return ThreadsService(client)


@router.post(
    "/scrape",
    response_model=ThreadsScrapeResponse,
    summary="Scrape Threads data",
    description="""
    Scrape Threads posts and profiles.

    **Options:**
    - `usernames`: List of usernames (without @)
    - `threadUrls`: Direct thread URLs
    - `searchQueries`: Search terms
    - `hashtags`: Hashtags (without #)

    At least one option must be provided.
    """,
)
async def scrape(
    request: ThreadsScrapeRequest,
    service: ThreadsService = Depends(get_service),
) -> ThreadsScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile/{username}",
    response_model=ThreadsScrapeResponse,
    summary="Scrape profile threads",
)
async def scrape_profile(
    username: str,
    limit: int = Query(default=20, ge=1, le=100),
    service: ThreadsService = Depends(get_service),
) -> ThreadsScrapeResponse:
    try:
        return await service.scrape_profile(username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/hashtag/{hashtag}",
    response_model=ThreadsScrapeResponse,
    summary="Scrape by hashtag",
)
async def scrape_hashtag(
    hashtag: str,
    limit: int = Query(default=20, ge=1, le=100),
    service: ThreadsService = Depends(get_service),
) -> ThreadsScrapeResponse:
    try:
        return await service.scrape_hashtag(hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=ThreadsScrapeResponse,
    summary="Search Threads",
)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    service: ThreadsService = Depends(get_service),
) -> ThreadsScrapeResponse:
    try:
        return await service.search(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/thread",
    response_model=ThreadsScrapeResponse,
    summary="Scrape specific thread",
)
async def scrape_thread(
    url: str = Query(..., description="Threads post URL"),
    include_replies: bool = Query(default=False),
    service: ThreadsService = Depends(get_service),
) -> ThreadsScrapeResponse:
    try:
        return await service.scrape_thread(url, include_replies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

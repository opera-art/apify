"""TikTok API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.tiktok import (
    TikTokService,
    TikTokScrapeRequest,
    TikTokScrapeResponse,
)

router = APIRouter(prefix="/tiktok", tags=["TikTok"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> TikTokService:
    return TikTokService(client)


@router.post(
    "/scrape",
    response_model=TikTokScrapeResponse,
    summary="Scrape TikTok data",
    description="""
    Scrape TikTok videos, profiles, and hashtags.

    **Options:**
    - `hashtags`: List of hashtags (without #)
    - `profiles`: List of usernames
    - `searchQueries`: Search terms
    - `videoUrls`: Direct video URLs

    At least one option must be provided.
    """,
)
async def scrape(
    request: TikTokScrapeRequest,
    service: TikTokService = Depends(get_service),
) -> TikTokScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/hashtag/{hashtag}",
    response_model=TikTokScrapeResponse,
    summary="Scrape by hashtag",
)
async def scrape_hashtag(
    hashtag: str,
    limit: int = Query(default=10, ge=1, le=100),
    service: TikTokService = Depends(get_service),
) -> TikTokScrapeResponse:
    try:
        return await service.scrape_hashtag(hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile/{username}",
    response_model=TikTokScrapeResponse,
    summary="Scrape profile",
)
async def scrape_profile(
    username: str,
    limit: int = Query(default=10, ge=1, le=100),
    service: TikTokService = Depends(get_service),
) -> TikTokScrapeResponse:
    try:
        return await service.scrape_profile(username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=TikTokScrapeResponse,
    summary="Search TikTok",
)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: TikTokService = Depends(get_service),
) -> TikTokScrapeResponse:
    try:
        return await service.search(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

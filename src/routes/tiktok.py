"""TikTok API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.tiktok import (
    TikTokResponse,
    scrape_hashtag,
    scrape_profile,
    search,
    get_video,
)

router = APIRouter(prefix="/tiktok", tags=["TikTok"])


@router.get(
    "/hashtag/{hashtag}",
    response_model=TikTokResponse,
    summary="Scrape videos by hashtag",
)
async def get_hashtag_videos(
    hashtag: str,
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> TikTokResponse:
    """Get TikTok videos by hashtag."""
    try:
        return await scrape_hashtag(client, hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile/{username}",
    response_model=TikTokResponse,
    summary="Scrape profile and videos",
)
async def get_profile_videos(
    username: str,
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> TikTokResponse:
    """Get TikTok profile and videos by username."""
    try:
        return await scrape_profile(client, username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=TikTokResponse,
    summary="Search TikTok",
)
async def search_tiktok(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> TikTokResponse:
    """Search TikTok videos."""
    try:
        return await search(client, q, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/video",
    response_model=TikTokResponse,
    summary="Get video details",
)
async def get_video_details(
    url: str = Query(..., description="TikTok video URL"),
    client: ApifyClient = Depends(get_apify_client),
) -> TikTokResponse:
    """Get TikTok video details by URL."""
    try:
        return await get_video(client, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""YouTube API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.youtube import (
    YouTubeService,
    YouTubeScrapeRequest,
    YouTubeScrapeResponse,
)

router = APIRouter(prefix="/youtube", tags=["YouTube"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> YouTubeService:
    return YouTubeService(client)


@router.post(
    "/scrape",
    response_model=YouTubeScrapeResponse,
    summary="Scrape YouTube data",
    description="""
    Scrape YouTube videos, channels, and playlists.

    **Options:**
    - `searchQueries`: Search terms
    - `channelUrls`: Channel URLs
    - `videoUrls`: Direct video URLs
    - `playlistUrls`: Playlist URLs

    At least one option must be provided.
    """,
)
async def scrape(
    request: YouTubeScrapeRequest,
    service: YouTubeService = Depends(get_service),
) -> YouTubeScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=YouTubeScrapeResponse,
    summary="Search YouTube",
)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=500),
    service: YouTubeService = Depends(get_service),
) -> YouTubeScrapeResponse:
    try:
        return await service.search(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/channel",
    response_model=YouTubeScrapeResponse,
    summary="Scrape channel videos",
)
async def scrape_channel(
    url: str = Query(..., description="YouTube channel URL"),
    limit: int = Query(default=50, ge=1, le=500),
    service: YouTubeService = Depends(get_service),
) -> YouTubeScrapeResponse:
    try:
        return await service.scrape_channel(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/video",
    response_model=YouTubeScrapeResponse,
    summary="Scrape video details",
)
async def scrape_video(
    url: str = Query(..., description="YouTube video URL"),
    include_comments: bool = Query(default=False),
    service: YouTubeService = Depends(get_service),
) -> YouTubeScrapeResponse:
    try:
        return await service.scrape_video(url, include_comments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/playlist",
    response_model=YouTubeScrapeResponse,
    summary="Scrape playlist videos",
)
async def scrape_playlist(
    url: str = Query(..., description="YouTube playlist URL"),
    limit: int = Query(default=50, ge=1, le=500),
    service: YouTubeService = Depends(get_service),
) -> YouTubeScrapeResponse:
    try:
        return await service.scrape_playlist(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

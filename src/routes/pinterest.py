"""Pinterest API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.pinterest import (
    PinterestService,
    PinterestScrapeRequest,
    PinterestScrapeResponse,
)

router = APIRouter(prefix="/pinterest", tags=["Pinterest"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> PinterestService:
    return PinterestService(client)


@router.post(
    "/scrape",
    response_model=PinterestScrapeResponse,
    summary="Scrape Pinterest data",
    description="""
    Scrape Pinterest pins, boards, and profiles.

    **Options:**
    - `pinUrls`: Direct pin URLs
    - `boardUrls`: Board URLs
    - `profileUrls`: Profile URLs
    - `searchQueries`: Search terms

    At least one option must be provided.
    """,
)
async def scrape(
    request: PinterestScrapeRequest,
    service: PinterestService = Depends(get_service),
) -> PinterestScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/board",
    response_model=PinterestScrapeResponse,
    summary="Scrape board pins",
)
async def scrape_board(
    url: str = Query(..., description="Pinterest board URL"),
    limit: int = Query(default=20, ge=1, le=200),
    service: PinterestService = Depends(get_service),
) -> PinterestScrapeResponse:
    try:
        return await service.scrape_board(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile",
    response_model=PinterestScrapeResponse,
    summary="Scrape profile pins",
)
async def scrape_profile(
    url: str = Query(..., description="Pinterest profile URL"),
    limit: int = Query(default=20, ge=1, le=200),
    service: PinterestService = Depends(get_service),
) -> PinterestScrapeResponse:
    try:
        return await service.scrape_profile(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=PinterestScrapeResponse,
    summary="Search Pinterest",
)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=200),
    service: PinterestService = Depends(get_service),
) -> PinterestScrapeResponse:
    try:
        return await service.search(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/pin",
    response_model=PinterestScrapeResponse,
    summary="Scrape specific pin",
)
async def scrape_pin(
    url: str = Query(..., description="Pinterest pin URL"),
    service: PinterestService = Depends(get_service),
) -> PinterestScrapeResponse:
    try:
        return await service.scrape_pin(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

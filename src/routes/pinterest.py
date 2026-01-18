"""Pinterest API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.pinterest import (
    PinterestResponse,
    scrape_board,
    scrape_profile,
    search,
    get_pin,
)

router = APIRouter(prefix="/pinterest", tags=["Pinterest"])


@router.get(
    "/board",
    response_model=PinterestResponse,
    summary="Scrape board pins",
)
async def get_board_pins(
    url: str = Query(..., description="Pinterest board URL"),
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> PinterestResponse:
    """Get pins from a Pinterest board."""
    try:
        return await scrape_board(client, url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile",
    response_model=PinterestResponse,
    summary="Scrape profile pins",
)
async def get_profile_pins(
    url: str = Query(..., description="Pinterest profile URL"),
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> PinterestResponse:
    """Get pins from a Pinterest profile."""
    try:
        return await scrape_profile(client, url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=PinterestResponse,
    summary="Search Pinterest",
)
async def search_pinterest(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> PinterestResponse:
    """Search Pinterest pins."""
    try:
        return await search(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/pin",
    response_model=PinterestResponse,
    summary="Get pin details",
)
async def get_pin_details(
    url: str = Query(..., description="Pinterest pin URL"),
    client: ApifyClient = Depends(get_apify_client),
) -> PinterestResponse:
    """Get Pinterest pin details."""
    try:
        return await get_pin(client, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

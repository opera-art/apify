"""LinkedIn API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.linkedin import (
    LinkedInService,
    LinkedInScrapeRequest,
    LinkedInScrapeResponse,
)

router = APIRouter(prefix="/linkedin", tags=["LinkedIn"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> LinkedInService:
    return LinkedInService(client)


@router.post(
    "/scrape",
    response_model=LinkedInScrapeResponse,
    summary="Scrape LinkedIn data",
    description="""
    Scrape LinkedIn posts from profiles and companies.

    **Options:**
    - `profileUrls`: LinkedIn profile URLs
    - `companyUrls`: Company page URLs
    - `searchQueries`: Search terms

    At least one option must be provided.
    """,
)
async def scrape(
    request: LinkedInScrapeRequest,
    service: LinkedInService = Depends(get_service),
) -> LinkedInScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/profile",
    response_model=LinkedInScrapeResponse,
    summary="Scrape profile posts",
)
async def scrape_profile_posts(
    url: str = Query(..., description="LinkedIn profile URL"),
    limit: int = Query(default=20, ge=1, le=100),
    service: LinkedInService = Depends(get_service),
) -> LinkedInScrapeResponse:
    try:
        return await service.scrape_profile_posts(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/company",
    response_model=LinkedInScrapeResponse,
    summary="Scrape company posts",
)
async def scrape_company_posts(
    url: str = Query(..., description="LinkedIn company URL"),
    limit: int = Query(default=20, ge=1, le=100),
    service: LinkedInService = Depends(get_service),
) -> LinkedInScrapeResponse:
    try:
        return await service.scrape_company_posts(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=LinkedInScrapeResponse,
    summary="Search LinkedIn posts",
)
async def search_posts(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    service: LinkedInService = Depends(get_service),
) -> LinkedInScrapeResponse:
    try:
        return await service.search_posts(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""Meta Ads (Facebook Ads) API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.meta_ads import (
    MetaAdsService,
    MetaAdsScrapeRequest,
    MetaAdsScrapeResponse,
    META_ADS_COUNTRIES,
)

router = APIRouter(prefix="/meta-ads", tags=["Meta Ads"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> MetaAdsService:
    return MetaAdsService(client)


@router.post(
    "/scrape",
    response_model=MetaAdsScrapeResponse,
    summary="Scrape Meta Ads data",
    description="""
    Scrape ads from Meta Ad Library.

    **Options:**
    - `pageUrls`: Facebook Page URLs
    - `adUrls`: Direct ad URLs
    - `searchTerms`: Keywords to search

    At least one option must be provided.
    """,
)
async def scrape(
    request: MetaAdsScrapeRequest,
    service: MetaAdsService = Depends(get_service),
) -> MetaAdsScrapeResponse:
    try:
        return await service.scrape(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/page",
    response_model=MetaAdsScrapeResponse,
    summary="Scrape ads from a Facebook Page",
)
async def scrape_page_ads(
    url: str = Query(..., description="Facebook Page URL"),
    limit: int = Query(default=50, ge=1, le=500),
    country: str = Query(default="ALL", description=f"Country code: {', '.join(META_ADS_COUNTRIES)}"),
    service: MetaAdsService = Depends(get_service),
) -> MetaAdsScrapeResponse:
    try:
        return await service.scrape_page_ads(url, limit, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=MetaAdsScrapeResponse,
    summary="Search ads in Ad Library",
)
async def search_ads(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=500),
    country: str = Query(default="ALL"),
    service: MetaAdsService = Depends(get_service),
) -> MetaAdsScrapeResponse:
    try:
        return await service.search_ads(q, limit, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/political",
    response_model=MetaAdsScrapeResponse,
    summary="Scrape political ads",
)
async def scrape_political_ads(
    country: str = Query(default="US"),
    limit: int = Query(default=50, ge=1, le=500),
    service: MetaAdsService = Depends(get_service),
) -> MetaAdsScrapeResponse:
    try:
        return await service.scrape_political_ads(country, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

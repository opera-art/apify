"""Meta Ads (Facebook Ads) API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.meta_ads import (
    MetaAdsResponse,
    META_ADS_COUNTRIES,
    scrape_page_ads,
    search_ads,
    scrape_political_ads,
)

router = APIRouter(prefix="/meta-ads", tags=["Meta Ads"])


@router.get(
    "/page",
    response_model=MetaAdsResponse,
    summary="Scrape ads from a Facebook Page",
)
async def get_page_ads(
    url: str = Query(..., description="Facebook Page URL"),
    limit: int = Query(default=50, ge=1, le=500),
    country: str = Query(default="ALL", description=f"Country code: {', '.join(META_ADS_COUNTRIES)}"),
    ad_type: str = Query(default="all", alias="adType"),
    client: ApifyClient = Depends(get_apify_client),
) -> MetaAdsResponse:
    """Get ads from a Facebook Page."""
    try:
        return await scrape_page_ads(client, url, limit, country, ad_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=MetaAdsResponse,
    summary="Search ads in Ad Library",
)
async def search_meta_ads(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=500),
    country: str = Query(default="ALL"),
    ad_type: str = Query(default="all", alias="adType"),
    client: ApifyClient = Depends(get_apify_client),
) -> MetaAdsResponse:
    """Search ads in the Meta Ad Library."""
    try:
        return await search_ads(client, q, limit, country, ad_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/political",
    response_model=MetaAdsResponse,
    summary="Scrape political ads",
)
async def get_political_ads(
    country: str = Query(default="US"),
    limit: int = Query(default=50, ge=1, le=500),
    client: ApifyClient = Depends(get_apify_client),
) -> MetaAdsResponse:
    """Get political and issue ads."""
    try:
        return await scrape_political_ads(client, country, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

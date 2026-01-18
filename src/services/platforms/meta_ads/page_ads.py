"""Meta Ads page ads scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import META_ADS_ACTOR_ID, META_ADS_DEFAULT_RESULTS, META_ADS_MAX_RESULTS
from .schemas import MetaAdsResponse
from .utils import run_actor


class MetaAdsPageRequest(BaseModel):
    """Request to scrape ads from a Facebook Page."""

    page_url: str = Field(
        alias="pageUrl",
        description="Facebook Page URL",
    )
    limit: int = Field(
        default=META_ADS_DEFAULT_RESULTS,
        ge=1,
        le=META_ADS_MAX_RESULTS,
    )
    country: str = Field(
        default="ALL",
        description="Country code for ad targeting",
    )
    ad_type: str = Field(
        default="all",
        alias="adType",
    )

    class Config:
        populate_by_name = True


def build_page_ads_input(request: MetaAdsPageRequest) -> dict:
    """Build the input payload for page ads scraping."""
    return {
        "startUrls": [{"url": request.page_url}],
        "maxAds": request.limit,
        "country": request.country,
        "adType": request.ad_type,
    }


async def scrape_page_ads(
    client: ApifyClient,
    page_url: str,
    limit: int = META_ADS_DEFAULT_RESULTS,
    country: str = "ALL",
    ad_type: str = "all",
) -> MetaAdsResponse:
    """
    Scrape ads from a Facebook Page.

    Args:
        client: Apify client instance
        page_url: Facebook Page URL
        limit: Maximum number of ads
        country: Country code
        ad_type: Type of ads

    Returns:
        MetaAdsResponse with page ads
    """
    request = MetaAdsPageRequest(
        page_url=page_url,
        limit=limit,
        country=country,
        ad_type=ad_type,
    )
    actor_input = build_page_ads_input(request)
    return run_actor(client, META_ADS_ACTOR_ID, actor_input)

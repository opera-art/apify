"""Meta Ads political ads scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import META_ADS_ACTOR_ID, META_ADS_DEFAULT_RESULTS, META_ADS_MAX_RESULTS
from .schemas import MetaAdsResponse
from .utils import run_actor


class MetaAdsPoliticalRequest(BaseModel):
    """Request to scrape political ads."""

    country: str = Field(
        default="US",
        description="Country code",
    )
    limit: int = Field(
        default=META_ADS_DEFAULT_RESULTS,
        ge=1,
        le=META_ADS_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_political_input(request: MetaAdsPoliticalRequest) -> dict:
    """Build the input payload for political ads scraping."""
    return {
        "searchTerms": ["*"],
        "maxAds": request.limit,
        "country": request.country,
        "adType": "political_and_issue_ads",
    }


async def scrape_political_ads(
    client: ApifyClient,
    country: str = "US",
    limit: int = META_ADS_DEFAULT_RESULTS,
) -> MetaAdsResponse:
    """
    Scrape political and issue ads.

    Args:
        client: Apify client instance
        country: Country code
        limit: Maximum number of ads

    Returns:
        MetaAdsResponse with political ads
    """
    request = MetaAdsPoliticalRequest(
        country=country,
        limit=limit,
    )
    actor_input = build_political_input(request)
    return run_actor(client, META_ADS_ACTOR_ID, actor_input)

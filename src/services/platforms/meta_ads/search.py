"""Meta Ads search service."""

from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import META_ADS_ACTOR_ID, META_ADS_DEFAULT_RESULTS, META_ADS_MAX_RESULTS
from .schemas import MetaAdsResponse
from .utils import run_actor


class MetaAdsSearchRequest(BaseModel):
    """Request to search ads in the Ad Library."""

    query: str = Field(description="Search query")
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
    start_date: Optional[date] = Field(
        default=None,
        alias="startDate",
    )
    end_date: Optional[date] = Field(
        default=None,
        alias="endDate",
    )

    class Config:
        populate_by_name = True


def build_search_input(request: MetaAdsSearchRequest) -> dict:
    """Build the input payload for ads search."""
    actor_input = {
        "searchTerms": [request.query],
        "maxAds": request.limit,
        "country": request.country,
        "adType": request.ad_type,
    }

    if request.start_date:
        actor_input["startDate"] = request.start_date.isoformat()

    if request.end_date:
        actor_input["endDate"] = request.end_date.isoformat()

    return actor_input


async def search_ads(
    client: ApifyClient,
    query: str,
    limit: int = META_ADS_DEFAULT_RESULTS,
    country: str = "ALL",
    ad_type: str = "all",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> MetaAdsResponse:
    """
    Search ads in the Ad Library.

    Args:
        client: Apify client instance
        query: Search query
        limit: Maximum number of ads
        country: Country code
        ad_type: Type of ads
        start_date: Filter ads from this date
        end_date: Filter ads until this date

    Returns:
        MetaAdsResponse with search results
    """
    request = MetaAdsSearchRequest(
        query=query,
        limit=limit,
        country=country,
        ad_type=ad_type,
        start_date=start_date,
        end_date=end_date,
    )
    actor_input = build_search_input(request)
    return run_actor(client, META_ADS_ACTOR_ID, actor_input)

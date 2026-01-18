"""TikTok request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional

from .constants import TIKTOK_DEFAULT_RESULTS, TIKTOK_MAX_RESULTS_PER_PAGE
from .types import TikTokSearchType, TikTokSortType


class TikTokHashtagRequest(BaseModel):
    """Request schema for TikTok hashtag scraping."""

    hashtag: str = Field(description="Hashtag to scrape (without #)")
    limit: int = Field(
        default=TIKTOK_DEFAULT_RESULTS,
        ge=1,
        le=TIKTOK_MAX_RESULTS_PER_PAGE,
    )

    class Config:
        populate_by_name = True


class TikTokProfileRequest(BaseModel):
    """Request schema for TikTok profile scraping."""

    username: str = Field(description="TikTok username to scrape")
    limit: int = Field(
        default=TIKTOK_DEFAULT_RESULTS,
        ge=1,
        le=TIKTOK_MAX_RESULTS_PER_PAGE,
    )

    class Config:
        populate_by_name = True


class TikTokSearchRequest(BaseModel):
    """Request schema for TikTok search."""

    query: str = Field(description="Search query")
    search_type: TikTokSearchType = Field(
        default=TikTokSearchType.TOP,
        alias="searchType",
    )
    limit: int = Field(
        default=TIKTOK_DEFAULT_RESULTS,
        ge=1,
        le=TIKTOK_MAX_RESULTS_PER_PAGE,
    )

    class Config:
        populate_by_name = True


class TikTokVideoRequest(BaseModel):
    """Request schema for TikTok video details."""

    url: str = Field(description="TikTok video URL")

    class Config:
        populate_by_name = True


class TikTokResponse(BaseModel):
    """Response schema for TikTok scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True

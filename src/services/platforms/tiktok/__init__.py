"""TikTok platform module."""

from .constants import (
    TIKTOK_ACTOR_ID,
    TIKTOK_DEFAULT_RESULTS,
    TIKTOK_MAX_RESULTS_PER_PAGE,
)
from .types import TikTokSearchType, TikTokSortType
from .schemas import (
    TikTokHashtagRequest,
    TikTokProfileRequest,
    TikTokSearchRequest,
    TikTokVideoRequest,
    TikTokResponse,
)
from .hashtag import scrape_hashtag
from .profile import scrape_profile
from .search import search
from .video import get_video

__all__ = [
    # Constants
    "TIKTOK_ACTOR_ID",
    "TIKTOK_DEFAULT_RESULTS",
    "TIKTOK_MAX_RESULTS_PER_PAGE",
    # Types
    "TikTokSearchType",
    "TikTokSortType",
    # Schemas
    "TikTokHashtagRequest",
    "TikTokProfileRequest",
    "TikTokSearchRequest",
    "TikTokVideoRequest",
    "TikTokResponse",
    # Functions
    "scrape_hashtag",
    "scrape_profile",
    "search",
    "get_video",
]

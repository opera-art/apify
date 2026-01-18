"""Meta Ads platform module."""

from .constants import (
    META_ADS_ACTOR_ID,
    META_ADS_DEFAULT_RESULTS,
    META_ADS_MAX_RESULTS,
    META_ADS_COUNTRIES,
    META_ADS_TYPES,
)
from .schemas import MetaAdsResponse

# Page Ads
from .page_ads import (
    MetaAdsPageRequest,
    scrape_page_ads,
)

# Search
from .search import (
    MetaAdsSearchRequest,
    search_ads,
)

# Political
from .political import (
    MetaAdsPoliticalRequest,
    scrape_political_ads,
)

__all__ = [
    # Constants
    "META_ADS_ACTOR_ID",
    "META_ADS_DEFAULT_RESULTS",
    "META_ADS_MAX_RESULTS",
    "META_ADS_COUNTRIES",
    "META_ADS_TYPES",
    # Schemas
    "MetaAdsResponse",
    "MetaAdsPageRequest",
    "MetaAdsSearchRequest",
    "MetaAdsPoliticalRequest",
    # Functions
    "scrape_page_ads",
    "search_ads",
    "scrape_political_ads",
]

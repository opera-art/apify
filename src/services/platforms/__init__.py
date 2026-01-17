"""
Platforms Module - Unified exports for all social media platform services.

This module provides a centralized interface for all platform-specific
scraping operations via Apify actors.

Supported Platforms:
- TikTok
- Instagram
- YouTube
- Meta Ads (Facebook Ads)
- Threads
- LinkedIn
- Pinterest
"""

from typing import Literal, Union
from apify_client import ApifyClient

# Import all platform modules
from .tiktok import (
    TikTokService,
    TikTokScrapeRequest,
    TikTokScrapeResponse,
    TikTokSearchType,
    TikTokSortType,
    TIKTOK_ACTOR_ID,
    validate_tiktok_request,
    build_tiktok_actor_input,
)

from .instagram import (
    InstagramService,
    InstagramScrapeRequest,
    InstagramScrapeResponse,
    InstagramSearchType,
    InstagramResultsType,
    INSTAGRAM_ACTOR_ID,
    validate_instagram_request,
    build_instagram_actor_input,
)

from .youtube import (
    YouTubeService,
    YouTubeScrapeRequest,
    YouTubeScrapeResponse,
    YOUTUBE_ACTOR_ID,
    validate_youtube_request,
    build_youtube_actor_input,
)

from .meta_ads import (
    MetaAdsService,
    MetaAdsScrapeRequest,
    MetaAdsScrapeResponse,
    META_ADS_ACTOR_ID,
    META_ADS_COUNTRIES,
    META_ADS_TYPES,
    validate_meta_ads_request,
    build_meta_ads_actor_input,
)

from .threads import (
    ThreadsService,
    ThreadsScrapeRequest,
    ThreadsScrapeResponse,
    THREADS_ACTOR_ID,
    validate_threads_request,
    build_threads_actor_input,
)

from .linkedin import (
    LinkedInService,
    LinkedInScrapeRequest,
    LinkedInScrapeResponse,
    LINKEDIN_ACTOR_ID,
    validate_linkedin_request,
    build_linkedin_actor_input,
)

from .pinterest import (
    PinterestService,
    PinterestScrapeRequest,
    PinterestScrapeResponse,
    PINTEREST_ACTOR_ID,
    validate_pinterest_request,
    build_pinterest_actor_input,
)


# =============================================================================
# PLATFORM TYPE DEFINITIONS
# =============================================================================

Platform = Literal[
    "tiktok",
    "instagram",
    "youtube",
    "meta_ads",
    "threads",
    "linkedin",
    "pinterest",
]

SUPPORTED_PLATFORMS: list[Platform] = [
    "tiktok",
    "instagram",
    "youtube",
    "meta_ads",
    "threads",
    "linkedin",
    "pinterest",
]

# Mapping of platform names to their Actor IDs
PLATFORM_ACTORS: dict[Platform, str] = {
    "tiktok": TIKTOK_ACTOR_ID,
    "instagram": INSTAGRAM_ACTOR_ID,
    "youtube": YOUTUBE_ACTOR_ID,
    "meta_ads": META_ADS_ACTOR_ID,
    "threads": THREADS_ACTOR_ID,
    "linkedin": LINKEDIN_ACTOR_ID,
    "pinterest": PINTEREST_ACTOR_ID,
}

# Union type for all request types
PlatformScrapeRequest = Union[
    TikTokScrapeRequest,
    InstagramScrapeRequest,
    YouTubeScrapeRequest,
    MetaAdsScrapeRequest,
    ThreadsScrapeRequest,
    LinkedInScrapeRequest,
    PinterestScrapeRequest,
]

# Union type for all response types
PlatformScrapeResponse = Union[
    TikTokScrapeResponse,
    InstagramScrapeResponse,
    YouTubeScrapeResponse,
    MetaAdsScrapeResponse,
    ThreadsScrapeResponse,
    LinkedInScrapeResponse,
    PinterestScrapeResponse,
]

# Union type for all service types
PlatformService = Union[
    TikTokService,
    InstagramService,
    YouTubeService,
    MetaAdsService,
    ThreadsService,
    LinkedInService,
    PinterestService,
]


# =============================================================================
# SERVICE FACTORY
# =============================================================================

def get_platform_service(platform: Platform, client: ApifyClient) -> PlatformService:
    """
    Factory function to get the appropriate service for a platform.

    Args:
        platform: The platform identifier
        client: Configured ApifyClient instance

    Returns:
        The appropriate platform service instance

    Raises:
        ValueError: If platform is not supported
    """
    services: dict[Platform, type] = {
        "tiktok": TikTokService,
        "instagram": InstagramService,
        "youtube": YouTubeService,
        "meta_ads": MetaAdsService,
        "threads": ThreadsService,
        "linkedin": LinkedInService,
        "pinterest": PinterestService,
    }

    if platform not in services:
        raise ValueError(f"Unsupported platform: {platform}. Supported: {SUPPORTED_PLATFORMS}")

    return services[platform](client)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Platform type
    "Platform",
    "SUPPORTED_PLATFORMS",
    "PLATFORM_ACTORS",
    # Union types
    "PlatformScrapeRequest",
    "PlatformScrapeResponse",
    "PlatformService",
    # Factory
    "get_platform_service",
    # TikTok
    "TikTokService",
    "TikTokScrapeRequest",
    "TikTokScrapeResponse",
    "TikTokSearchType",
    "TikTokSortType",
    "TIKTOK_ACTOR_ID",
    "validate_tiktok_request",
    "build_tiktok_actor_input",
    # Instagram
    "InstagramService",
    "InstagramScrapeRequest",
    "InstagramScrapeResponse",
    "InstagramSearchType",
    "InstagramResultsType",
    "INSTAGRAM_ACTOR_ID",
    "validate_instagram_request",
    "build_instagram_actor_input",
    # YouTube
    "YouTubeService",
    "YouTubeScrapeRequest",
    "YouTubeScrapeResponse",
    "YOUTUBE_ACTOR_ID",
    "validate_youtube_request",
    "build_youtube_actor_input",
    # Meta Ads
    "MetaAdsService",
    "MetaAdsScrapeRequest",
    "MetaAdsScrapeResponse",
    "META_ADS_ACTOR_ID",
    "META_ADS_COUNTRIES",
    "META_ADS_TYPES",
    "validate_meta_ads_request",
    "build_meta_ads_actor_input",
    # Threads
    "ThreadsService",
    "ThreadsScrapeRequest",
    "ThreadsScrapeResponse",
    "THREADS_ACTOR_ID",
    "validate_threads_request",
    "build_threads_actor_input",
    # LinkedIn
    "LinkedInService",
    "LinkedInScrapeRequest",
    "LinkedInScrapeResponse",
    "LINKEDIN_ACTOR_ID",
    "validate_linkedin_request",
    "build_linkedin_actor_input",
    # Pinterest
    "PinterestService",
    "PinterestScrapeRequest",
    "PinterestScrapeResponse",
    "PINTEREST_ACTOR_ID",
    "validate_pinterest_request",
    "build_pinterest_actor_input",
]

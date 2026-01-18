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

from typing import Literal

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

# =============================================================================
# TIKTOK IMPORTS
# =============================================================================

from .tiktok import (
    TIKTOK_ACTOR_ID,
    TIKTOK_DEFAULT_RESULTS,
    TikTokResponse,
    TikTokSearchType,
    TikTokSortType,
    scrape_hashtag as tiktok_scrape_hashtag,
    scrape_profile as tiktok_scrape_profile,
    search as tiktok_search,
    get_video as tiktok_get_video,
)

# =============================================================================
# INSTAGRAM IMPORTS
# =============================================================================

from .instagram import (
    INSTAGRAM_ACTOR_ID,
    INSTAGRAM_DEFAULT_RESULTS,
    InstagramResponse,
    InstagramSearchType,
    InstagramResultsType,
    get_profile as instagram_get_profile,
    scrape_profiles as instagram_scrape_profiles,
    get_user_posts as instagram_get_user_posts,
    scrape_posts as instagram_scrape_posts,
    get_post_comments as instagram_get_post_comments,
    scrape_comments as instagram_scrape_comments,
    get_hashtag_posts as instagram_get_hashtag_posts,
    scrape_hashtag as instagram_scrape_hashtag,
    get_user_reels as instagram_get_user_reels,
    scrape_reels as instagram_scrape_reels,
    get_post_details as instagram_get_post_details,
    scrape_post_details as instagram_scrape_post_details,
    search as instagram_search,
    search_users as instagram_search_users,
    search_hashtags as instagram_search_hashtags,
    search_places as instagram_search_places,
)

# =============================================================================
# YOUTUBE IMPORTS
# =============================================================================

from .youtube import (
    YOUTUBE_ACTOR_ID,
    YOUTUBE_DEFAULT_RESULTS,
    YouTubeResponse,
    search as youtube_search,
    scrape_channel as youtube_scrape_channel,
    get_video as youtube_get_video,
    scrape_playlist as youtube_scrape_playlist,
)

# =============================================================================
# META ADS IMPORTS
# =============================================================================

from .meta_ads import (
    META_ADS_ACTOR_ID,
    META_ADS_DEFAULT_RESULTS,
    META_ADS_COUNTRIES,
    META_ADS_TYPES,
    MetaAdsResponse,
    scrape_page_ads as meta_ads_scrape_page_ads,
    search_ads as meta_ads_search_ads,
    scrape_political_ads as meta_ads_scrape_political_ads,
)

# =============================================================================
# THREADS IMPORTS
# =============================================================================

from .threads import (
    THREADS_ACTOR_ID,
    THREADS_DEFAULT_RESULTS,
    ThreadsResponse,
    scrape_profile as threads_scrape_profile,
    scrape_hashtag as threads_scrape_hashtag,
    search as threads_search,
    get_thread as threads_get_thread,
)

# =============================================================================
# LINKEDIN IMPORTS
# =============================================================================

from .linkedin import (
    LINKEDIN_ACTOR_ID,
    LINKEDIN_DEFAULT_RESULTS,
    LinkedInResponse,
    scrape_profile_posts as linkedin_scrape_profile_posts,
    scrape_company_posts as linkedin_scrape_company_posts,
    search_posts as linkedin_search_posts,
)

# =============================================================================
# PINTEREST IMPORTS
# =============================================================================

from .pinterest import (
    PINTEREST_ACTOR_ID,
    PINTEREST_DEFAULT_RESULTS,
    PinterestResponse,
    scrape_board as pinterest_scrape_board,
    scrape_profile as pinterest_scrape_profile,
    search as pinterest_search,
    get_pin as pinterest_get_pin,
)

# =============================================================================
# PLATFORM ACTORS MAPPING
# =============================================================================

PLATFORM_ACTORS: dict[Platform, str] = {
    "tiktok": TIKTOK_ACTOR_ID,
    "instagram": INSTAGRAM_ACTOR_ID,
    "youtube": YOUTUBE_ACTOR_ID,
    "meta_ads": META_ADS_ACTOR_ID,
    "threads": THREADS_ACTOR_ID,
    "linkedin": LINKEDIN_ACTOR_ID,
    "pinterest": PINTEREST_ACTOR_ID,
}

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Platform type
    "Platform",
    "SUPPORTED_PLATFORMS",
    "PLATFORM_ACTORS",
    # TikTok
    "TIKTOK_ACTOR_ID",
    "TIKTOK_DEFAULT_RESULTS",
    "TikTokResponse",
    "TikTokSearchType",
    "TikTokSortType",
    "tiktok_scrape_hashtag",
    "tiktok_scrape_profile",
    "tiktok_search",
    "tiktok_get_video",
    # Instagram
    "INSTAGRAM_ACTOR_ID",
    "INSTAGRAM_DEFAULT_RESULTS",
    "InstagramResponse",
    "InstagramSearchType",
    "InstagramResultsType",
    "instagram_get_profile",
    "instagram_scrape_profiles",
    "instagram_get_user_posts",
    "instagram_scrape_posts",
    "instagram_get_post_comments",
    "instagram_scrape_comments",
    "instagram_get_hashtag_posts",
    "instagram_scrape_hashtag",
    "instagram_get_user_reels",
    "instagram_scrape_reels",
    "instagram_get_post_details",
    "instagram_scrape_post_details",
    "instagram_search",
    "instagram_search_users",
    "instagram_search_hashtags",
    "instagram_search_places",
    # YouTube
    "YOUTUBE_ACTOR_ID",
    "YOUTUBE_DEFAULT_RESULTS",
    "YouTubeResponse",
    "youtube_search",
    "youtube_scrape_channel",
    "youtube_get_video",
    "youtube_scrape_playlist",
    # Meta Ads
    "META_ADS_ACTOR_ID",
    "META_ADS_DEFAULT_RESULTS",
    "META_ADS_COUNTRIES",
    "META_ADS_TYPES",
    "MetaAdsResponse",
    "meta_ads_scrape_page_ads",
    "meta_ads_search_ads",
    "meta_ads_scrape_political_ads",
    # Threads
    "THREADS_ACTOR_ID",
    "THREADS_DEFAULT_RESULTS",
    "ThreadsResponse",
    "threads_scrape_profile",
    "threads_scrape_hashtag",
    "threads_search",
    "threads_get_thread",
    # LinkedIn
    "LINKEDIN_ACTOR_ID",
    "LINKEDIN_DEFAULT_RESULTS",
    "LinkedInResponse",
    "linkedin_scrape_profile_posts",
    "linkedin_scrape_company_posts",
    "linkedin_search_posts",
    # Pinterest
    "PINTEREST_ACTOR_ID",
    "PINTEREST_DEFAULT_RESULTS",
    "PinterestResponse",
    "pinterest_scrape_board",
    "pinterest_scrape_profile",
    "pinterest_search",
    "pinterest_get_pin",
]

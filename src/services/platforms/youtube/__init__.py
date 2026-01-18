"""YouTube platform module."""

from .constants import (
    YOUTUBE_ACTOR_ID,
    YOUTUBE_DEFAULT_RESULTS,
    YOUTUBE_MAX_RESULTS,
)
from .schemas import YouTubeResponse

# Search
from .search import (
    YouTubeSearchRequest,
    search,
)

# Channel
from .channel import (
    YouTubeChannelRequest,
    scrape_channel,
)

# Video
from .video import (
    YouTubeVideoRequest,
    get_video,
)

# Playlist
from .playlist import (
    YouTubePlaylistRequest,
    scrape_playlist,
)

__all__ = [
    # Constants
    "YOUTUBE_ACTOR_ID",
    "YOUTUBE_DEFAULT_RESULTS",
    "YOUTUBE_MAX_RESULTS",
    # Schemas
    "YouTubeResponse",
    "YouTubeSearchRequest",
    "YouTubeChannelRequest",
    "YouTubeVideoRequest",
    "YouTubePlaylistRequest",
    # Functions
    "search",
    "scrape_channel",
    "get_video",
    "scrape_playlist",
]

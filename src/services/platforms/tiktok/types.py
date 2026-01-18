"""TikTok types and enums."""

from enum import Enum


class TikTokSearchType(str, Enum):
    VIDEO = "video"
    USER = "user"
    TOP = "top"


class TikTokSortType(str, Enum):
    LATEST = "latest"
    OLDEST = "oldest"
    POPULAR = "popular"

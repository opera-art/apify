"""Instagram types and enums."""

from enum import Enum


class InstagramSearchType(str, Enum):
    USER = "user"
    HASHTAG = "hashtag"
    PLACE = "place"


class InstagramResultsType(str, Enum):
    POSTS = "posts"
    DETAILS = "details"
    COMMENTS = "comments"

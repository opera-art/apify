"""Threads thread details service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import THREADS_ACTOR_ID
from .schemas import ThreadsResponse
from .utils import run_actor


class ThreadsThreadRequest(BaseModel):
    """Request to get thread details."""

    thread_url: str = Field(
        alias="threadUrl",
        description="Threads post URL",
    )
    include_replies: bool = Field(
        default=False,
        alias="includeReplies",
    )

    class Config:
        populate_by_name = True


def build_thread_input(request: ThreadsThreadRequest) -> dict:
    """Build the input payload for thread details."""
    actor_input = {
        "threadUrls": [request.thread_url],
        "maxItems": 1,
    }

    if request.include_replies:
        actor_input["includeReplies"] = True

    return actor_input


async def get_thread(
    client: ApifyClient,
    thread_url: str,
    include_replies: bool = False,
) -> ThreadsResponse:
    """
    Get thread details.

    Args:
        client: Apify client instance
        thread_url: Threads post URL
        include_replies: Include replies

    Returns:
        ThreadsResponse with thread details
    """
    request = ThreadsThreadRequest(
        thread_url=thread_url,
        include_replies=include_replies,
    )
    actor_input = build_thread_input(request)
    return run_actor(client, THREADS_ACTOR_ID, actor_input)

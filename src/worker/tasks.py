"""Celery tasks for background processing."""

from apify_client import ApifyClient
from src.worker.celery_app import celery_app
from src.config import get_settings


def get_client() -> ApifyClient:
    """Get Apify client instance."""
    settings = get_settings()
    return ApifyClient(settings.apify_api_key)


def run_apify_actor(actor_id: str, actor_input: dict) -> dict:
    """Execute an Apify actor and return results."""
    client = get_client()
    run = client.actor(actor_id).call(run_input=actor_input)

    dataset_id = run.get("defaultDatasetId")
    items = []

    if dataset_id:
        dataset_items = client.dataset(dataset_id).list_items()
        items = dataset_items.items

    return {
        "success": True,
        "data": items,
        "total_results": len(items),
        "run_id": run.get("id"),
    }


# =============================================================================
# INSTAGRAM TASKS
# =============================================================================

@celery_app.task(bind=True, name="instagram.scrape_posts")
def instagram_scrape_posts(self, usernames: list[str], limit: int = 20):
    """Scrape Instagram posts in background."""
    from src.services.platforms.instagram.constants import INSTAGRAM_ACTOR_ID
    from src.services.platforms.instagram.utils import get_default_proxy

    direct_urls = [f"https://www.instagram.com/{u}/" for u in usernames]

    actor_input = {
        "directUrls": direct_urls,
        "resultsType": "posts",
        "resultsLimit": limit,
        "proxy": get_default_proxy(),
    }

    return run_apify_actor(INSTAGRAM_ACTOR_ID, actor_input)


@celery_app.task(bind=True, name="instagram.scrape_profile")
def instagram_scrape_profile(self, usernames: list[str]):
    """Scrape Instagram profiles in background."""
    from src.services.platforms.instagram.constants import INSTAGRAM_PROFILE_ACTOR_ID
    from src.services.platforms.instagram.utils import get_default_proxy

    actor_input = {
        "usernames": usernames,
        "proxy": get_default_proxy(),
    }

    return run_apify_actor(INSTAGRAM_PROFILE_ACTOR_ID, actor_input)


@celery_app.task(bind=True, name="instagram.scrape_hashtag")
def instagram_scrape_hashtag(self, hashtags: list[str], limit: int = 20):
    """Scrape Instagram hashtags in background."""
    from src.services.platforms.instagram.constants import INSTAGRAM_HASHTAG_ACTOR_ID
    from src.services.platforms.instagram.utils import get_default_proxy

    actor_input = {
        "hashtags": hashtags,
        "resultsLimit": limit,
        "proxy": get_default_proxy(),
    }

    return run_apify_actor(INSTAGRAM_HASHTAG_ACTOR_ID, actor_input)


@celery_app.task(bind=True, name="instagram.scrape_comments")
def instagram_scrape_comments(self, post_urls: list[str], limit: int = 100):
    """Scrape Instagram comments in background."""
    from src.services.platforms.instagram.constants import INSTAGRAM_ACTOR_ID
    from src.services.platforms.instagram.utils import get_default_proxy

    actor_input = {
        "directUrls": post_urls,
        "resultsType": "comments",
        "resultsLimit": limit,
        "proxy": get_default_proxy(),
    }

    return run_apify_actor(INSTAGRAM_ACTOR_ID, actor_input)


# =============================================================================
# TIKTOK TASKS
# =============================================================================

@celery_app.task(bind=True, name="tiktok.scrape_hashtag")
def tiktok_scrape_hashtag(self, hashtag: str, limit: int = 10):
    """Scrape TikTok hashtag in background."""
    from src.services.platforms.tiktok.constants import TIKTOK_ACTOR_ID

    actor_input = {
        "hashtags": [hashtag],
        "resultsPerPage": limit,
    }

    return run_apify_actor(TIKTOK_ACTOR_ID, actor_input)


@celery_app.task(bind=True, name="tiktok.scrape_profile")
def tiktok_scrape_profile(self, username: str, limit: int = 10):
    """Scrape TikTok profile in background."""
    from src.services.platforms.tiktok.constants import TIKTOK_ACTOR_ID

    actor_input = {
        "profiles": [username],
        "resultsPerPage": limit,
    }

    return run_apify_actor(TIKTOK_ACTOR_ID, actor_input)


# =============================================================================
# YOUTUBE TASKS
# =============================================================================

@celery_app.task(bind=True, name="youtube.search")
def youtube_search(self, query: str, limit: int = 10):
    """Search YouTube in background."""
    from src.services.platforms.youtube.constants import YOUTUBE_ACTOR_ID

    actor_input = {
        "searchKeywords": query,
        "maxResults": limit,
    }

    return run_apify_actor(YOUTUBE_ACTOR_ID, actor_input)


@celery_app.task(bind=True, name="youtube.scrape_channel")
def youtube_scrape_channel(self, channel_url: str, limit: int = 10):
    """Scrape YouTube channel in background."""
    from src.services.platforms.youtube.constants import YOUTUBE_ACTOR_ID

    actor_input = {
        "startUrls": [{"url": channel_url}],
        "maxResults": limit,
    }

    return run_apify_actor(YOUTUBE_ACTOR_ID, actor_input)

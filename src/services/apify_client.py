from apify_client import ApifyClient
from src.config import get_settings


def get_apify_client() -> ApifyClient:
    """Get configured Apify client instance."""
    settings = get_settings()
    return ApifyClient(settings.apify_api_token)

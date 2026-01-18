from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    tiktok,
    instagram,
    youtube,
    meta_ads,
    threads,
    linkedin,
    pinterest,
    jobs,
)

app = FastAPI(
    title="Social Media Scraper API",
    description="""
    API para scraping de dados de redes sociais usando Apify.

    ## Plataformas suportadas:

    - **TikTok** - Videos, perfis, hashtags e buscas
    - **Instagram** - Posts, perfis, comentarios, reels, hashtags e buscas
    - **YouTube** - Videos, canais, playlists e buscas
    - **Meta Ads** - Anuncios do Facebook/Instagram Ad Library
    - **Threads** - Posts, perfis, hashtags e buscas
    - **LinkedIn** - Posts de perfis e empresas
    - **Pinterest** - Pins, boards, perfis e buscas

    ## Autenticacao
    Configure a variavel de ambiente `APIFY_API_TOKEN` com seu token da Apify.

    ## Arquitetura
    Cada plataforma tem endpoints separados por responsabilidade:
    - `/profile` - Metadados do perfil
    - `/posts` - Posts/conteudos
    - `/comments` - Comentarios
    - `/search` - Buscas
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all platform routers
app.include_router(tiktok.router, prefix="/api/v1")
app.include_router(instagram.router, prefix="/api/v1")
app.include_router(youtube.router, prefix="/api/v1")
app.include_router(meta_ads.router, prefix="/api/v1")
app.include_router(threads.router, prefix="/api/v1")
app.include_router(linkedin.router, prefix="/api/v1")
app.include_router(pinterest.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "message": "Social Media Scraper API",
        "platforms": [
            "tiktok",
            "instagram",
            "youtube",
            "meta_ads",
            "threads",
            "linkedin",
            "pinterest",
        ],
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@app.get("/platforms", tags=["Info"])
async def list_platforms():
    """List all supported platforms and their endpoints."""
    return {
        "platforms": {
            "tiktok": {
                "description": "TikTok video and profile scraping",
                "endpoints": ["/hashtag", "/profile", "/search", "/scrape"],
            },
            "instagram": {
                "description": "Instagram posts, reels, comments, and profiles",
                "endpoints": [
                    "/profile",
                    "/posts",
                    "/comments",
                    "/hashtag",
                    "/reels",
                    "/post-details",
                    "/search/users",
                    "/search/hashtags",
                    "/search/places",
                ],
            },
            "youtube": {
                "description": "YouTube videos, channels, and playlists",
                "endpoints": ["/search", "/channel", "/video", "/playlist", "/scrape"],
            },
            "meta_ads": {
                "description": "Facebook/Instagram Ad Library scraping",
                "endpoints": ["/page", "/search", "/political", "/scrape"],
            },
            "threads": {
                "description": "Threads posts and profiles",
                "endpoints": ["/profile", "/hashtag", "/search", "/thread", "/scrape"],
            },
            "linkedin": {
                "description": "LinkedIn posts from profiles and companies",
                "endpoints": ["/profile", "/company", "/search", "/scrape"],
            },
            "pinterest": {
                "description": "Pinterest pins, boards, and profiles",
                "endpoints": ["/board", "/profile", "/search", "/pin", "/scrape"],
            },
        }
    }

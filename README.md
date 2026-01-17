# Social Media Scraper API

API para scraping de dados de redes sociais usando Apify.

## Plataformas suportadas

- **TikTok** - Videos, perfis, hashtags e buscas
- **Instagram** - Posts, perfis, comentarios, reels, hashtags e buscas
- **YouTube** - Videos, canais, playlists e buscas
- **Meta Ads** - Anuncios do Facebook/Instagram Ad Library
- **Threads** - Posts, perfis, hashtags e buscas
- **LinkedIn** - Posts de perfis e empresas
- **Pinterest** - Pins, boards, perfis e buscas

## Instalacao

```bash
pip install -r requirements.txt
```

## Configuracao

Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Configure sua chave da API Apify:

```
APIFY_API_TOKEN=your_token_here
```

## Executando

```bash
uvicorn src.main:app --reload
```

A API estara disponivel em `http://localhost:8000`

## Documentacao

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### TikTok (`/api/v1/tiktok`)
- `POST /scrape` - Scrape generico
- `GET /hashtag/{hashtag}` - Videos por hashtag
- `GET /profile/{username}` - Perfil e videos
- `GET /search` - Buscar videos

### Instagram (`/api/v1/instagram`)
- `GET /profile/{username}` - Metadados do perfil
- `GET /posts/{username}` - Posts do usuario
- `GET /comments` - Comentarios de um post
- `GET /hashtag/{hashtag}` - Posts por hashtag
- `GET /reels/{username}` - Reels do usuario
- `GET /post-details` - Detalhes de um post
- `GET /search/users` - Buscar usuarios
- `GET /search/hashtags` - Buscar hashtags
- `GET /search/places` - Buscar lugares

### YouTube (`/api/v1/youtube`)
- `POST /scrape` - Scrape generico
- `GET /search` - Buscar videos
- `GET /channel` - Videos de um canal
- `GET /video` - Detalhes de um video
- `GET /playlist` - Videos de uma playlist

### Meta Ads (`/api/v1/meta-ads`)
- `POST /scrape` - Scrape generico
- `GET /page` - Anuncios de uma pagina
- `GET /search` - Buscar anuncios
- `GET /political` - Anuncios politicos

### Threads (`/api/v1/threads`)
- `POST /scrape` - Scrape generico
- `GET /profile/{username}` - Posts do perfil
- `GET /hashtag/{hashtag}` - Posts por hashtag
- `GET /search` - Buscar posts
- `GET /thread` - Detalhes de um thread

### LinkedIn (`/api/v1/linkedin`)
- `POST /scrape` - Scrape generico
- `GET /profile` - Posts de um perfil
- `GET /company` - Posts de uma empresa
- `GET /search` - Buscar posts

### Pinterest (`/api/v1/pinterest`)
- `POST /scrape` - Scrape generico
- `GET /board` - Pins de um board
- `GET /profile` - Pins de um perfil
- `GET /search` - Buscar pins
- `GET /pin` - Detalhes de um pin

## Arquitetura

```
src/
├── main.py                 # FastAPI app
├── config.py               # Settings
├── routes/                 # API routes
│   ├── tiktok.py
│   ├── instagram.py
│   ├── youtube.py
│   ├── meta_ads.py
│   ├── threads.py
│   ├── linkedin.py
│   └── pinterest.py
└── services/
    ├── apify_client.py     # Apify client factory
    └── platforms/          # Platform services
        ├── tiktok.py
        ├── instagram.py
        ├── youtube.py
        ├── meta_ads.py
        ├── threads.py
        ├── linkedin.py
        └── pinterest.py
```

## Licenca

MIT

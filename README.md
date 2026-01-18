# Social Media Scraper API

API para scraping de dados de redes sociais usando Apify, com suporte a processamento em background para escalabilidade.

**URL de Produção:** https://apify.viol1n.com

## Plataformas Suportadas

| Plataforma | Descrição |
|------------|-----------|
| **TikTok** | Videos, perfis, hashtags e buscas |
| **Instagram** | Posts, perfis, comentários, reels, hashtags e buscas |
| **YouTube** | Videos, canais, playlists e buscas |
| **Meta Ads** | Anúncios do Facebook/Instagram Ad Library |
| **Threads** | Posts, perfis, hashtags e buscas |
| **LinkedIn** | Posts de perfis e empresas |
| **Pinterest** | Pins, boards, perfis e buscas |

## Arquitetura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Cliente/App   │────▶│   FastAPI API   │────▶│   Apify Actors  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               │ (Jobs Async)
                               ▼
                        ┌─────────────────┐
                        │      Redis      │
                        │ (Message Broker)│
                        └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Celery Worker  │────▶ Apify Actors
                        └─────────────────┘
```

## Estrutura do Projeto

```
dados/
├── src/
│   ├── main.py                    # FastAPI app principal
│   ├── config.py                  # Configurações (env vars)
│   ├── routes/
│   │   ├── tiktok.py             # Rotas TikTok
│   │   ├── instagram.py          # Rotas Instagram
│   │   ├── youtube.py            # Rotas YouTube
│   │   ├── meta_ads.py           # Rotas Meta Ads
│   │   ├── threads.py            # Rotas Threads
│   │   ├── linkedin.py           # Rotas LinkedIn
│   │   ├── pinterest.py          # Rotas Pinterest
│   │   └── jobs.py               # Rotas Background Jobs
│   ├── services/
│   │   ├── apify_client.py       # Cliente Apify
│   │   └── platforms/
│   │       ├── tiktok/
│   │       ├── instagram/
│   │       ├── youtube/
│   │       ├── meta_ads/
│   │       ├── threads/
│   │       ├── linkedin/
│   │       └── pinterest/
│   └── worker/
│       ├── __init__.py
│       ├── celery_app.py         # Configuração Celery
│       └── tasks.py              # Tasks de background
├── requirements.txt
├── Procfile
└── README.md
```

## Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `APIFY_API_KEY` | Token da API Apify | Sim |
| `REDIS_URL` | URL de conexão Redis | Sim (para jobs) |

### Instalação Local

```bash
# Clonar repositório
git clone https://github.com/jaianmenezes/dados.git
cd dados

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Iniciar API
uvicorn src.main:app --reload

# Em outro terminal, iniciar worker (requer Redis)
celery -A src.worker.celery_app worker --loglevel=info
```

## Uso da API

### Documentação Interativa

- **Swagger UI**: https://apify.viol1n.com/docs
- **ReDoc**: https://apify.viol1n.com/redoc
- **OpenAPI JSON**: https://apify.viol1n.com/openapi.json

### Endpoints Síncronos (Resposta Imediata)

Todos os endpoints de plataforma retornam dados diretamente:

```bash
# Perfil Instagram
curl "https://apify.viol1n.com/api/v1/instagram/profile?username=natgeo"

# Posts TikTok por hashtag
curl "https://apify.viol1n.com/api/v1/tiktok/hashtag?hashtag=brasil&limit=10"

# Busca YouTube
curl "https://apify.viol1n.com/api/v1/youtube/search?query=python&limit=5"
```

### Endpoints por Plataforma

#### TikTok (`/api/v1/tiktok`)
- `POST /scrape` - Scrape genérico
- `GET /hashtag/{hashtag}` - Videos por hashtag
- `GET /profile/{username}` - Perfil e videos
- `GET /search` - Buscar videos

#### Instagram (`/api/v1/instagram`)
- `GET /profile/{username}` - Metadados do perfil
- `GET /posts/{username}` - Posts do usuário
- `GET /comments` - Comentários de um post
- `GET /hashtag/{hashtag}` - Posts por hashtag
- `GET /reels/{username}` - Reels do usuário
- `GET /post-details` - Detalhes de um post
- `GET /search/users` - Buscar usuários
- `GET /search/hashtags` - Buscar hashtags
- `GET /search/places` - Buscar lugares

#### YouTube (`/api/v1/youtube`)
- `POST /scrape` - Scrape genérico
- `GET /search` - Buscar videos
- `GET /channel` - Videos de um canal
- `GET /video` - Detalhes de um video
- `GET /playlist` - Videos de uma playlist

#### Meta Ads (`/api/v1/meta-ads`)
- `POST /scrape` - Scrape genérico
- `GET /page` - Anúncios de uma página
- `GET /search` - Buscar anúncios
- `GET /political` - Anúncios políticos

#### Threads (`/api/v1/threads`)
- `POST /scrape` - Scrape genérico
- `GET /profile/{username}` - Posts do perfil
- `GET /hashtag/{hashtag}` - Posts por hashtag
- `GET /search` - Buscar posts
- `GET /thread` - Detalhes de um thread

#### LinkedIn (`/api/v1/linkedin`)
- `POST /scrape` - Scrape genérico
- `GET /profile` - Posts de um perfil
- `GET /company` - Posts de uma empresa
- `GET /search` - Buscar posts

#### Pinterest (`/api/v1/pinterest`)
- `POST /scrape` - Scrape genérico
- `GET /board` - Pins de um board
- `GET /profile` - Pins de um perfil
- `GET /search` - Buscar pins
- `GET /pin` - Detalhes de um pin

---

## Background Jobs (Processamento Assíncrono)

Para operações que podem demorar ou para alta concorrência, use os endpoints de jobs.

### Jobs Disponíveis

| Método | Endpoint | Body |
|--------|----------|------|
| POST | `/api/v1/jobs/instagram/posts` | `{"usernames": [...], "limit": 20}` |
| POST | `/api/v1/jobs/instagram/profile` | `{"usernames": [...]}` |
| POST | `/api/v1/jobs/instagram/hashtag` | `{"hashtags": [...], "limit": 20}` |
| POST | `/api/v1/jobs/tiktok/hashtag` | `{"hashtag": "...", "limit": 10}` |
| POST | `/api/v1/jobs/youtube/search` | `{"query": "...", "limit": 10}` |
| GET | `/api/v1/jobs/{job_id}` | - |

### Fluxo de Uso

#### 1. Submeter Job

```bash
curl -X POST "https://apify.viol1n.com/api/v1/jobs/instagram/posts" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["natgeo", "bbcnews"], "limit": 20}'
```

**Resposta:**
```json
{
  "job_id": "68ff8ff8-79d9-47f6-953f-c0e5d45626f0",
  "status": "PENDING",
  "message": "Job submitted. Check status at /api/v1/jobs/68ff8ff8-79d9-47f6-953f-c0e5d45626f0"
}
```

#### 2. Verificar Status

```bash
curl "https://apify.viol1n.com/api/v1/jobs/68ff8ff8-79d9-47f6-953f-c0e5d45626f0"
```

**Status possíveis:**
| Status | Descrição |
|--------|-----------|
| `PENDING` | Job na fila aguardando |
| `STARTED` | Job em execução |
| `SUCCESS` | Job concluído com sucesso |
| `FAILURE` | Job falhou |

#### 3. Obter Resultado

Quando `status = SUCCESS`, o campo `result` contém os dados:

```json
{
  "job_id": "68ff8ff8-79d9-47f6-953f-c0e5d45626f0",
  "status": "SUCCESS",
  "result": {
    "success": true,
    "data": [...],
    "total_results": 5,
    "run_id": "YGVmEYL7IWHMfG2bt"
  },
  "error": null
}
```

### Exemplo Completo (TikTok Hashtag)

```bash
# 1. Submeter job
curl -X POST "https://apify.viol1n.com/api/v1/jobs/tiktok/hashtag" \
  -H "Content-Type: application/json" \
  -d '{"hashtag": "brasil", "limit": 5}'

# Resposta: {"job_id": "abc123...", "status": "PENDING", ...}

# 2. Aguardar e verificar status (repetir até SUCCESS)
curl "https://apify.viol1n.com/api/v1/jobs/abc123..."

# 3. Quando SUCCESS, o resultado estará no campo "result"
```

---

## Deploy no Railway

### Serviços Configurados

| Serviço | Função | Start Command |
|---------|--------|---------------|
| **apify-api** | API FastAPI | `uvicorn src.main:app --host 0.0.0.0 --port $PORT` |
| **celery-worker** | Processamento background | `celery -A src.worker.celery_app worker --loglevel=info` |
| **redis** | Message broker + cache | (gerenciado pelo Railway) |

### IDs do Projeto Railway

```
Project ID:     df323476-a932-4b78-bd75-d08774868696
Environment ID: 5330018b-2141-4f43-a10e-5ba572178631

Services:
- apify-api:      87bf919f-51f6-4313-8f16-093f3e16343e
- celery-worker:  d4554aeb-91e2-4664-974e-0baab3176a6a
- redis:          d1744218-ad7e-474f-acd8-1d9fa2fff328
```

### Variáveis de Ambiente no Railway

**apify-api e celery-worker:**
```
APIFY_API_KEY=seu_token_apify
REDIS_URL=redis://default:${{redis.REDIS_PASSWORD}}@redis.railway.internal:6379
```

---

## Escalabilidade

O sistema foi projetado para SaaS com múltiplos usuários simultâneos:

### Estratégias Implementadas

1. **Jobs em Background**: Operações pesadas são processadas pelo Celery Worker
2. **Redis como Broker**: Fila de mensagens para distribuir trabalho
3. **Stateless API**: Permite escalar horizontalmente adicionando mais instâncias
4. **Polling de Status**: Cliente verifica status sem bloquear a API

### Fluxo para Alta Concorrência

```
User A ─┐                    ┌── Worker processa Job A
User B ──┼──▶ API ──▶ Redis ──┼── Worker processa Job B
User C ─┘                    └── Worker processa Job C
```

### Escalando no Railway

Para aumentar capacidade:
1. **Mais Workers**: Duplique o serviço `celery-worker`
2. **Redis Cluster**: Upgrade para Redis com mais memória
3. **API Replicas**: Configure múltiplas réplicas do `apify-api`

---

## Desenvolvimento

### Adicionar Nova Plataforma

1. Criar pasta em `src/services/platforms/nova_plataforma/`
2. Criar `constants.py` com IDs dos actors Apify
3. Criar `service.py` com funções de scraping
4. Criar rota em `src/routes/nova_plataforma.py`
5. Registrar router em `src/main.py`

### Adicionar Novo Job

1. Criar task em `src/worker/tasks.py`:
```python
@celery_app.task(bind=True, name="plataforma.acao")
def plataforma_acao(self, param1, param2):
    # implementação
    return run_apify_actor(ACTOR_ID, actor_input)
```

2. Criar endpoint em `src/routes/jobs.py`:
```python
@router.post("/plataforma/acao")
def submit_job(request: RequestSchema):
    task = tasks.plataforma_acao.delay(...)
    return JobSubmitResponse(job_id=task.id, ...)
```

---

## Banco de Dados (Supabase)

Os dados coletados são armazenados no Supabase, no schema `apify`.

### Arquitetura do Schema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SCHEMA: apify                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────┐                                                 │
│  │   scraping_jobs    │  ◄── Controle de todos os jobs                  │
│  └─────────┬──────────┘                                                 │
│            │                                                             │
│            ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    TABELAS POR TIPO DE CONTEÚDO                  │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │                                                                   │    │
│  │  ┌──────────────────┐  Perfis de todas as plataformas            │    │
│  │  │ scraped_profiles │  (IG, TikTok, YT, Threads, LinkedIn, Pinterest) │
│  │  └──────────────────┘                                             │    │
│  │                                                                   │    │
│  │  ┌──────────────────┐  Posts, vídeos, reels, pins, threads       │    │
│  │  │  scraped_posts   │  (todas plataformas exceto Meta Ads)       │    │
│  │  └──────────────────┘                                             │    │
│  │                                                                   │    │
│  │  ┌──────────────────┐  Comentários                               │    │
│  │  │ scraped_comments │  (IG, YouTube, LinkedIn, TikTok)           │    │
│  │  └──────────────────┘                                             │    │
│  │                                                                   │    │
│  │  ┌──────────────────┐  Anúncios do Meta Ads Library              │    │
│  │  │   scraped_ads    │                                             │    │
│  │  └──────────────────┘                                             │    │
│  │                                                                   │    │
│  │  ┌──────────────────┐  Boards do Pinterest                       │    │
│  │  │  scraped_boards  │                                             │    │
│  │  └──────────────────┘                                             │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    TABELA DE HISTÓRICO                           │    │
│  │  ┌────────────────────────┐                                      │    │
│  │  │ profile_metrics_history │  Evolução de métricas (time-series) │    │
│  │  └────────────────────────┘                                      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Tabelas

#### 1. `apify.scraping_jobs` - Controle de Jobs

Registra todos os jobs de scraping executados.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único do job |
| `clerk_org_id` | TEXT | ID da organização (multi-tenant) |
| `clerk_user_id` | TEXT | ID do usuário que solicitou |
| `platform` | TEXT | tiktok, instagram, youtube, meta_ads, threads, linkedin, pinterest |
| `operation` | TEXT | Tipo de operação (profile, posts, hashtag, search, etc) |
| `input_params` | JSONB | Parâmetros enviados para o scraping |
| `status` | TEXT | pending, started, success, failure |
| `celery_job_id` | TEXT | ID do job no Celery |
| `apify_run_id` | TEXT | ID do run no Apify |
| `total_results` | INT | Quantidade de resultados |
| `credits_used` | INT | Créditos consumidos |
| `error_message` | TEXT | Mensagem de erro (se falhou) |
| `created_at` | TIMESTAMPTZ | Data de criação |
| `started_at` | TIMESTAMPTZ | Data de início |
| `completed_at` | TIMESTAMPTZ | Data de conclusão |

#### 2. `apify.scraped_profiles` - Perfis Coletados

Perfis de usuários, canais e empresas de todas as plataformas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `job_id` | UUID | FK para scraping_jobs |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | Plataforma de origem |
| `external_id` | TEXT | ID na plataforma original |
| `username` | TEXT | Nome de usuário |
| `display_name` | TEXT | Nome de exibição |
| `profile_url` | TEXT | URL do perfil |
| `avatar_url` | TEXT | URL do avatar |
| `bio` | TEXT | Biografia |
| `website` | TEXT | Website |
| `location` | TEXT | Localização |
| `followers_count` | INT | Seguidores |
| `following_count` | INT | Seguindo |
| `posts_count` | INT | Total de posts |
| `is_verified` | BOOL | Conta verificada |
| `is_business` | BOOL | Conta comercial |
| `is_private` | BOOL | Conta privada |
| `extra_data` | JSONB | Dados específicos da plataforma |
| `scraped_at` | TIMESTAMPTZ | Data da coleta |

**Constraint:** `UNIQUE(platform, external_id)`

#### 3. `apify.scraped_posts` - Posts e Vídeos

Posts, vídeos, reels, pins, threads de todas as plataformas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `job_id` | UUID | FK para scraping_jobs |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | Plataforma de origem |
| `content_type` | TEXT | post, video, reel, story, short, thread, pin, article |
| `external_id` | TEXT | ID na plataforma original |
| `external_url` | TEXT | URL do conteúdo |
| `author_id` | TEXT | ID do autor |
| `author_username` | TEXT | Username do autor |
| `content_text` | TEXT | Texto/legenda |
| `title` | TEXT | Título (YouTube, Pinterest) |
| `media_urls` | JSONB | URLs de mídia (imagens, vídeos) |
| `thumbnail_url` | TEXT | URL da thumbnail |
| `likes_count` | INT | Curtidas |
| `comments_count` | INT | Comentários |
| `shares_count` | INT | Compartilhamentos |
| `views_count` | INT | Visualizações |
| `saves_count` | INT | Salvos |
| `reposts_count` | INT | Reposts |
| `hashtags` | TEXT[] | Array de hashtags |
| `mentions` | TEXT[] | Array de menções |
| `duration_seconds` | INT | Duração (vídeos) |
| `extra_data` | JSONB | Dados específicos da plataforma |
| `published_at` | TIMESTAMPTZ | Data de publicação |
| `scraped_at` | TIMESTAMPTZ | Data da coleta |

**Constraint:** `UNIQUE(platform, external_id)`

#### 4. `apify.scraped_comments` - Comentários

Comentários coletados de posts.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `job_id` | UUID | FK para scraping_jobs |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | instagram, youtube, linkedin, tiktok |
| `external_id` | TEXT | ID do comentário |
| `post_external_id` | TEXT | ID do post relacionado |
| `post_url` | TEXT | URL do post |
| `author_id` | TEXT | ID do autor |
| `author_username` | TEXT | Username do autor |
| `author_display_name` | TEXT | Nome do autor |
| `author_avatar_url` | TEXT | Avatar do autor |
| `content_text` | TEXT | Texto do comentário |
| `likes_count` | INT | Curtidas |
| `replies_count` | INT | Respostas |
| `is_reply` | BOOL | É uma resposta |
| `parent_comment_id` | TEXT | ID do comentário pai |
| `published_at` | TIMESTAMPTZ | Data de publicação |
| `scraped_at` | TIMESTAMPTZ | Data da coleta |

**Constraint:** `UNIQUE(platform, external_id)`

#### 5. `apify.scraped_ads` - Anúncios

Anúncios do Meta Ads Library.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `job_id` | UUID | FK para scraping_jobs |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | meta_ads, google_ads, tiktok_ads |
| `external_id` | TEXT | ID do anúncio |
| `advertiser_id` | TEXT | ID do anunciante |
| `advertiser_name` | TEXT | Nome do anunciante |
| `page_id` | TEXT | ID da página |
| `page_name` | TEXT | Nome da página |
| `ad_text` | TEXT | Texto do anúncio |
| `ad_title` | TEXT | Título |
| `media_urls` | JSONB | URLs de mídia |
| `thumbnail_url` | TEXT | Thumbnail |
| `landing_url` | TEXT | URL de destino |
| `cta_type` | TEXT | Tipo de CTA |
| `spend_lower` | INT | Gasto mínimo estimado |
| `spend_upper` | INT | Gasto máximo estimado |
| `spend_currency` | TEXT | Moeda (default: BRL) |
| `impressions_lower` | INT | Impressões mín |
| `impressions_upper` | INT | Impressões máx |
| `targeting_data` | JSONB | Dados de segmentação |
| `demographics` | JSONB | Demografia |
| `regions` | TEXT[] | Regiões |
| `ad_type` | TEXT | Tipo do anúncio |
| `is_political` | BOOL | Anúncio político |
| `funding_entity` | TEXT | Entidade financiadora |
| `start_date` | DATE | Data início |
| `end_date` | DATE | Data fim |
| `is_active` | BOOL | Está ativo |
| `scraped_at` | TIMESTAMPTZ | Data da coleta |

**Constraint:** `UNIQUE(platform, external_id)`

#### 6. `apify.scraped_boards` - Boards do Pinterest

Boards coletados do Pinterest.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `job_id` | UUID | FK para scraping_jobs |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | pinterest |
| `external_id` | TEXT | ID do board |
| `name` | TEXT | Nome do board |
| `description` | TEXT | Descrição |
| `board_url` | TEXT | URL do board |
| `cover_image_url` | TEXT | Imagem de capa |
| `owner_id` | TEXT | ID do dono |
| `owner_username` | TEXT | Username do dono |
| `pins_count` | INT | Quantidade de pins |
| `followers_count` | INT | Seguidores |
| `collaborators_count` | INT | Colaboradores |
| `is_private` | BOOL | É privado |
| `is_collaborative` | BOOL | É colaborativo |
| `category` | TEXT | Categoria |
| `created_at_platform` | TIMESTAMPTZ | Data criação na plataforma |
| `scraped_at` | TIMESTAMPTZ | Data da coleta |

**Constraint:** `UNIQUE(platform, external_id)`

#### 7. `apify.profile_metrics_history` - Histórico de Métricas

Histórico de métricas de perfis para análise de evolução (time-series).

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID | ID único |
| `profile_id` | UUID | FK para scraped_profiles |
| `clerk_org_id` | TEXT | ID da organização |
| `platform` | TEXT | Plataforma |
| `profile_external_id` | TEXT | ID do perfil na plataforma |
| `username` | TEXT | Username |
| `followers_count` | INT | Seguidores |
| `following_count` | INT | Seguindo |
| `posts_count` | INT | Posts |
| `followers_change` | INT | Variação de seguidores |
| `following_change` | INT | Variação de seguindo |
| `posts_change` | INT | Variação de posts |
| `engagement_rate` | NUMERIC | Taxa de engajamento |
| `recorded_at` | TIMESTAMPTZ | Data do registro |

### Segurança (RLS)

Todas as tabelas têm **Row Level Security (RLS)** habilitado com políticas baseadas em `clerk_org_id`:

```sql
-- Usuários só podem ver dados da sua organização
CREATE POLICY "Users can view their org data" ON apify.tabela
    FOR SELECT USING (clerk_org_id = current_setting('request.jwt.claims', true)::json->>'org_id');
```

### Queries Úteis

```sql
-- Jobs recentes de uma organização
SELECT * FROM apify.scraping_jobs
WHERE clerk_org_id = 'org_xxx'
ORDER BY created_at DESC
LIMIT 10;

-- Posts mais curtidos por plataforma
SELECT platform, author_username, content_text, likes_count
FROM apify.scraped_posts
WHERE clerk_org_id = 'org_xxx'
ORDER BY likes_count DESC
LIMIT 10;

-- Evolução de seguidores de um perfil
SELECT recorded_at, followers_count, followers_change
FROM apify.profile_metrics_history
WHERE profile_id = 'uuid_xxx'
ORDER BY recorded_at;

-- Buscar posts por hashtag
SELECT * FROM apify.scraped_posts
WHERE 'brasil' = ANY(hashtags)
AND platform = 'instagram';

-- Anúncios ativos de uma página
SELECT * FROM apify.scraped_ads
WHERE page_name ILIKE '%coca-cola%'
AND is_active = true;
```

### Supabase Project

```
Project ID:  vlrkieseassxjrrbbsmb
Project:     social-media
Region:      us-east-1
Schema:      apify
```

---

## Licença

MIT

## Autor

Jaian Menezes - [@jaianmenezes](https://github.com/jaianmenezes)

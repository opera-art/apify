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

## Licença

MIT

## Autor

Jaian Menezes - [@jaianmenezes](https://github.com/jaianmenezes)

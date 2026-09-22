# URL Shortener Cheat Sheet

## One-Sentence Explanation

This is a FastAPI backend that creates short URLs, redirects users to the original URLs, tracks click analytics in PostgreSQL, and uses Redis to cache frequent short-code lookups.

## Best 30-Second Explanation

"I built a URL shortener with FastAPI, PostgreSQL, Redis, and Docker. Users submit a long URL and get back a short code. When someone visits the short link, the app checks Redis first, falls back to PostgreSQL if needed, records a click event, and redirects to the original URL. I also added tests and Docker Compose so the API, database, and cache can run together."

## Memorize These Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Check API health |
| `POST /api/urls` | Create a short URL |
| `GET /{short_code}` | Redirect to original URL |
| `GET /api/urls/{short_code}/stats` | View analytics |

## Most Important Flow

```text
POST long URL
-> validate URL
-> generate unique code
-> save in PostgreSQL
-> return short URL

GET short code
-> check Redis
-> if missing, check PostgreSQL
-> cache result in Redis
-> record click in PostgreSQL
-> redirect user
```

## Database Tables

`short_urls`

- `id`
- `short_code`
- `original_url`
- `created_at`
- `is_active`

`click_events`

- `id`
- `url_id`
- `clicked_at`
- `ip_address`
- `user_agent`
- `referrer`

## Why Each Tool Was Used

- FastAPI: REST API and automatic docs.
- PostgreSQL: permanent relational storage.
- Redis: fast cache for common redirects.
- Docker: run API, database, and cache together.
- Pytest: verify the core behavior.

## Key Commands

Open the project:

```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\URL Shortener Interview Kit\url-shortener-analytics-service"
```

Run with Docker:

```powershell
copy .env.example .env
docker compose up --build
```

Open docs:

```text
http://localhost:8000/docs
```

Run tests:

```powershell
.\.venv\Scripts\python -m pytest
```

## Be Honest About This

Implemented:

- URL creation
- Redirects
- Click tracking
- PostgreSQL models
- Redis caching
- Docker Compose
- Core tests

Not implemented:

- Login/authentication
- User accounts
- Rate limiting
- Custom domains
- Frontend dashboard
- Alembic migrations
- Production monitoring

## Best Improvement Answer

"The next improvements I would make are Alembic migrations, rate limiting, authentication for analytics, custom aliases, link expiration, and moving heavy analytics processing to a queue if traffic became high."

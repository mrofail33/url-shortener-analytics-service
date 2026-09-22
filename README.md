# URL Shortener & Analytics Service

A clean, beginner-friendly portfolio project built with **Python, FastAPI, PostgreSQL, Redis, and Docker**.

The service creates short URLs, redirects users to the original destination, stores URL and click data in PostgreSQL, and uses Redis to cache frequently requested short codes.

## Features

- Create unique short URLs with a REST API
- Redirect short codes to original URLs
- Store URLs in PostgreSQL
- Track click analytics with timestamp, IP address, user agent, and referrer
- Cache short-code lookups in Redis to reduce database reads
- Health check endpoint
- Docker Compose setup for API, PostgreSQL, and Redis
- Tests for core create, redirect, analytics, and error behavior

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Docker and Docker Compose
- Pytest

## Project Structure

```text
url-shortener-analytics-service/
├── app/
│   ├── api/
│   │   ├── router.py
│   │   └── routes/
│   │       ├── health.py
│   │       └── urls.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── click.py
│   │   └── url.py
│   ├── schemas/
│   │   └── url.py
│   ├── services/
│   │   ├── cache.py
│   │   ├── shortener.py
│   │   └── urls.py
│   └── main.py
├── tests/
│   └── test_urls.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start With Docker

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Start the API, PostgreSQL, and Redis:

```bash
docker compose up --build
```

3. Open the interactive API docs:

```text
http://localhost:8000/docs
```

4. Check the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## API Examples

### Create a Short URL

```bash
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d "{\"original_url\":\"https://example.com/articles/fastapi\"}"
```

Example response:

```json
{
  "id": 1,
  "original_url": "https://example.com/articles/fastapi",
  "short_code": "aB3xY9q",
  "short_url": "http://localhost:8000/aB3xY9q",
  "created_at": "2026-09-22T18:00:00Z"
}
```

### Redirect to the Original URL

```bash
curl -i http://localhost:8000/aB3xY9q
```

The API returns a redirect response and records a click event.

### View URL Analytics

```bash
curl http://localhost:8000/api/urls/aB3xY9q/stats
```

Example response:

```json
{
  "id": 1,
  "original_url": "https://example.com/articles/fastapi",
  "short_code": "aB3xY9q",
  "short_url": "http://localhost:8000/aB3xY9q",
  "created_at": "2026-09-22T18:00:00Z",
  "click_count": 3,
  "recent_clicks": [
    {
      "clicked_at": "2026-09-22T18:03:00Z",
      "ip_address": "127.0.0.1",
      "user_agent": "curl/8.0.0",
      "referrer": null
    }
  ]
}
```

## Running Tests

Install dependencies locally:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

The tests use SQLite in memory so they can run quickly without starting PostgreSQL.

## Architecture Explanation

The app is split into small layers:

- **Routes** receive HTTP requests and return responses.
- **Schemas** validate request and response data.
- **Models** define database tables.
- **Services** hold business logic such as creating short codes, reading from Redis, writing click events, and querying analytics.
- **Database session** manages the SQLAlchemy connection.
- **Config** reads environment variables from `.env`.

## Database and Cache Flow

### Creating a short URL

1. Client sends an original URL to `POST /api/urls`.
2. FastAPI validates that the value is a valid HTTP or HTTPS URL.
3. The service generates a random short code.
4. The URL and short code are saved in PostgreSQL.
5. The API returns the short code and complete short URL.

### Redirecting a short URL

1. Client visits `GET /{short_code}`.
2. The API checks Redis for the short code.
3. If Redis has it, the API uses the cached original URL.
4. If Redis misses, the API reads PostgreSQL and then stores the result in Redis.
5. The API records a click event in PostgreSQL.
6. The API redirects the client to the original URL.

Redis is used as a performance improvement. PostgreSQL remains the source of truth.

## Error Handling

- Invalid URLs return FastAPI validation errors.
- Unknown short codes return `404 Short URL not found`.
- Redis failures do not break redirects because the API can still use PostgreSQL.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `APP_NAME` | Display name for the FastAPI app |
| `APP_ENV` | Current environment name |
| `BASE_URL` | Base URL used when returning short links |
| `DATABASE_URL` | SQLAlchemy database connection string |
| `REDIS_URL` | Redis connection string |
| `REDIS_TTL_SECONDS` | How long cached short-code lookups stay in Redis |
| `SHORT_CODE_LENGTH` | Number of characters in generated short codes |

## How to Explain This in an Interview

"I built a URL shortener API with FastAPI. When a user submits a long URL, the app validates it, creates a unique short code, and stores the mapping in PostgreSQL. When someone visits the short code, the app first checks Redis for a cached lookup. If it is not cached, it loads the URL from PostgreSQL and then stores it in Redis for faster future redirects. Each redirect also creates a click analytics record with a timestamp and simple request metadata. I containerized the API, PostgreSQL, and Redis with Docker Compose so the project can be started consistently on any machine."

## Resume-Ready Bullets

**URL Shortener & Analytics Service | Python, FastAPI, PostgreSQL, Redis, Docker**

- Developed a REST API that generates unique shortened URLs and redirects users to their original destinations.
- Implemented PostgreSQL persistence and click analytics to track URL creation and redirect activity.
- Added Redis caching for frequently accessed URLs to reduce unnecessary database queries.
- Containerized application services with Docker for consistent development and deployment.

## Notes for Beginners

This project intentionally avoids heavy production features like authentication, rate limiting, background jobs, and database migrations. Those are good future improvements, but the current version keeps the core system clear and easy to explain.

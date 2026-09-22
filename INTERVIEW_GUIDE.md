# URL Shortener & Analytics Service - Interview Guide

## Simple Project Summary

This project is a backend API that turns long URLs into short URLs.

Example:

- Original URL: `https://www.python.org`
- Short URL: `http://localhost:8000/abc123X`

When someone visits the short URL, the app redirects them to the original URL and records a click event for analytics.

## The Main Idea

The app has three main jobs:

1. Create a short code for a long URL.
2. Redirect short codes back to the original URL.
3. Track click analytics every time a short link is used.

## Tech Stack

### FastAPI

FastAPI is used to build the REST API. It is beginner-friendly, fast, and automatically creates interactive API docs at `/docs`.

### PostgreSQL

PostgreSQL stores the important permanent data:

- The original URL
- The generated short code
- When the short URL was created
- Click events for analytics

PostgreSQL is the source of truth.

### Redis

Redis is used as a cache for short-code lookups.

When someone visits a short URL, the app first checks Redis. If Redis already knows the original URL, the app can redirect faster without asking PostgreSQL.

If Redis is down or misses, the app still works by using PostgreSQL.

### Docker

Docker Compose runs the API, PostgreSQL, and Redis together. This makes the project easier to run on another machine because the services are defined in one setup.

## Architecture

```text
Browser or API client
        |
        v
FastAPI routes
        |
        v
Service layer
        |
        +--> PostgreSQL stores URL and click data
        |
        +--> Redis caches short-code lookups
```

## Request Flow

### Creating a Short URL

Endpoint: `POST /api/urls`

1. The user sends an original URL.
2. FastAPI validates that it is an HTTP or HTTPS URL.
3. The service generates a random 7-character short code.
4. The app checks PostgreSQL to make sure the code is not already used.
5. The app saves the original URL and short code in PostgreSQL.
6. The API returns the short code and full short URL.

### Redirecting a Short URL

Endpoint: `GET /{short_code}`

1. The user visits a short URL.
2. The app checks Redis for `url:{short_code}`.
3. If Redis has the URL, that is a cache hit.
4. If Redis does not have it, that is a cache miss, so the app queries PostgreSQL.
5. After a database lookup, the app saves the result in Redis for future redirects.
6. The app records a click event in PostgreSQL.
7. The app sends a `307 Temporary Redirect` to the original URL.

### Click Analytics Flow

Every successful redirect creates a row in the `click_events` table.

The app stores:

- Timestamp
- URL id
- IP address if available
- User agent if available
- Referrer if available

Endpoint: `GET /api/urls/{short_code}/stats`

This endpoint returns the original URL, short code, click count, and up to 10 recent clicks.

## Database Schema

### `short_urls`

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `short_code` | Unique short code, indexed |
| `original_url` | Destination URL |
| `created_at` | When the short URL was created |
| `is_active` | Allows links to be disabled later |

### `click_events`

| Field | Purpose |
| --- | --- |
| `id` | Primary key |
| `url_id` | Foreign key to `short_urls.id` |
| `clicked_at` | When the redirect happened |
| `ip_address` | Simple request metadata |
| `user_agent` | Browser/client metadata |
| `referrer` | Where the request came from, if sent |

## Redis Cache Hit/Miss Flow

### Cache Hit

1. Short code exists in Redis.
2. App uses the cached original URL.
3. App records a click.
4. App redirects the user.

### Cache Miss

1. Short code is not in Redis.
2. App queries PostgreSQL.
3. If found, app stores the URL data in Redis.
4. App records a click.
5. App redirects the user.

### Cache Expiration

Cached values expire after `REDIS_TTL_SECONDS`, which defaults to 3600 seconds.

That means Redis speeds up common lookups but does not permanently replace the database.

## REST Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Confirms the API is running |
| `POST` | `/api/urls` | Creates a short URL |
| `GET` | `/{short_code}` | Redirects to the original URL |
| `GET` | `/api/urls/{short_code}/stats` | Shows click analytics |

## Error Handling

- Invalid URLs are rejected by FastAPI/Pydantic validation.
- Missing short codes return `404 Short URL not found`.
- Redis errors do not crash redirects; the app falls back to PostgreSQL.
- User agent and referrer strings are shortened before saving so they fit the database fields.

## Major Files And Folders

| Path | What it does |
| --- | --- |
| `app/main.py` | Creates the FastAPI app and database tables |
| `app/api/routes/urls.py` | Defines create, redirect, and stats endpoints |
| `app/api/routes/health.py` | Defines the health check |
| `app/models/url.py` | Defines the `short_urls` database table |
| `app/models/click.py` | Defines the `click_events` database table |
| `app/schemas/url.py` | Defines request/response validation models |
| `app/services/shortener.py` | Generates unique short codes |
| `app/services/urls.py` | Contains main URL and analytics logic |
| `app/services/cache.py` | Reads/writes Redis cache values |
| `app/core/config.py` | Reads environment variables |
| `app/db/session.py` | Creates database connection/session |
| `tests/test_urls.py` | Tests create, redirect, analytics, and 404 behavior |
| `docker-compose.yml` | Runs API, PostgreSQL, and Redis |
| `Dockerfile` | Builds the API container |
| `.env.example` | Example environment settings |

## Docker Setup

Docker Compose starts three services:

- `api`: the FastAPI app
- `postgres`: the PostgreSQL database
- `redis`: the Redis cache

Basic commands:

```powershell
copy .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

## Best Interview Explanation

"I built a URL shortener API with FastAPI. A user sends a long URL, the app validates it, creates a unique short code, and stores the mapping in PostgreSQL. When someone visits the short link, the app checks Redis first for a cached lookup. If Redis misses, it loads the URL from PostgreSQL and then caches it. Each redirect also writes a click event to PostgreSQL so the stats endpoint can show click count and recent click metadata. I used Docker Compose so the API, PostgreSQL, and Redis can run together consistently."

## What Not To Overclaim

Do not say this project has authentication, rate limiting, custom domains, migrations, user accounts, background jobs, or production monitoring. Those are good future improvements, but they are not currently implemented.

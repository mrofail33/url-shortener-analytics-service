# Interview Proof

Safe interview claim:

> I built a FastAPI URL shortener with PostgreSQL persistence, Redis lookup caching, redirect click analytics, Docker Compose, and tests for the core API behavior.

## What the repo proves

- `POST /api/urls` creates a short URL.
- `GET /{short_code}` redirects and records a click.
- `GET /api/urls/{short_code}/stats` returns click analytics.
- PostgreSQL is the source of truth through SQLAlchemy models.
- Redis is a cache only; the app still works if Redis is unavailable.
- Docker Compose starts the API, PostgreSQL, and Redis together.
- `tests/test_urls.py` covers create, redirect, stats, and missing short code behavior.
- `.github/workflows/ci.yml` runs the test suite on every push and pull request.

## What not to claim yet

- Production URL safety scanning.
- Authentication or user accounts.
- Rate limiting.
- Custom domains.
- Alembic migrations.
- Production monitoring.

## Simple next upgrade

Add rate limiting and a small URL safety check that blocks non-HTTP schemes and private-network destinations.

# URL Shortener Interview Questions

## Tell me about this project.

I built a URL Shortener and Analytics Service using FastAPI, PostgreSQL, Redis, and Docker. Users can submit a long URL and get back a short URL. When someone visits the short URL, the app redirects them to the original destination and records a click event. Redis is used to speed up repeated short-code lookups, while PostgreSQL stores the permanent URL and analytics data.

## Why did you build it?

I wanted a project that shows backend fundamentals clearly: REST APIs, validation, database persistence, caching, analytics, testing, and Docker-based setup.

## Why FastAPI?

FastAPI is simple to use, has strong request validation through Pydantic, and automatically generates API docs at `/docs`, which makes the project easy to demo.

## Why PostgreSQL?

PostgreSQL is a reliable relational database. This project has structured data with relationships: one short URL can have many click events. PostgreSQL is a good fit for that.

## Why Redis?

Redirects can happen often, and each redirect needs to look up the original URL. Redis can cache that lookup so popular links do not always need a database query.

## What is the source of truth?

PostgreSQL is the source of truth. Redis is only a temporary performance cache.

## What happens on a cache hit?

The short code is found in Redis, so the app uses the cached original URL, records the click in PostgreSQL, and redirects the user.

## What happens on a cache miss?

The app checks PostgreSQL. If the short code exists, it stores the URL data in Redis for future requests, records the click, and redirects the user.

## How does cache expiration work?

The cached short-code data is saved with `setex`, which means it has a time-to-live. The default is 3600 seconds. After that, Redis removes it and the app can fetch it from PostgreSQL again.

## How are short-code collisions handled?

The app generates a random 7-character code and checks PostgreSQL to see if it already exists. If it exists, the app generates another one. The database also has a uniqueness constraint on `short_code`.

## What endpoints did you build?

- `GET /health` checks that the API is running.
- `POST /api/urls` creates a short URL.
- `GET /{short_code}` redirects to the original URL.
- `GET /api/urls/{short_code}/stats` returns analytics.

## What data is tracked for analytics?

Each redirect records a click event with a timestamp, the related URL id, IP address if available, user agent if available, and referrer if available.

## What was a technical challenge?

One challenge was keeping Redis useful without making it required. The app catches Redis errors and falls back to PostgreSQL, so redirects can still work even if the cache is unavailable.

## How does validation work?

The create endpoint uses a Pydantic schema with `AnyHttpUrl`, so invalid URLs are rejected before the app tries to save them.

## How does the app handle missing short codes?

If a short code is not found, the app returns `404 Short URL not found`.

## How did you test it?

The test file covers creating a short URL, redirecting and recording a click, returning stats, and returning 404 for a missing code. The tests use SQLite in memory so they run quickly without needing PostgreSQL.

## How would you scale it?

I would keep using Redis for hot links, add rate limiting, add database migrations, run multiple API containers behind a load balancer, and add monitoring. For very high traffic, analytics writes could move to a queue so redirects stay fast.

## How would you improve security?

I would add rate limiting, block unsafe or malicious destination URLs, add authentication for analytics, protect admin-style endpoints, and avoid exposing sensitive configuration.

## What would you improve next?

I would add database migrations with Alembic, custom aliases, link expiration, user accounts, rate limiting, better analytics dashboards, and deployment instructions for a cloud provider.

## Is this production-ready?

It is a strong portfolio project, but not fully production-ready. It intentionally keeps the core logic easy to understand. Production improvements would include migrations, authentication, rate limiting, observability, and stronger security checks.

## How do you explain Docker here?

Docker Compose defines the API, PostgreSQL, and Redis services in one file. That means another developer can start the whole system with one command instead of installing and configuring every service manually.

## What should you avoid saying?

Avoid saying it has login, rate limiting, custom domains, a frontend dashboard, or production monitoring. Those are not implemented in this version.

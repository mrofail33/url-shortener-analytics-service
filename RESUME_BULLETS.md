# Resume-Ready Bullets

## Project Line

**URL Shortener & Analytics Service | Python, FastAPI, PostgreSQL, Redis, Docker**

## Resume Bullets

- Developed a REST API that generates unique shortened URLs and redirects users to their original destinations.
- Implemented PostgreSQL persistence and click analytics to track URL creation and redirect activity.
- Added Redis caching for frequently accessed URLs to reduce unnecessary database queries.
- Containerized application services with Docker Compose for consistent local development and deployment.

## Slightly More Detailed Version

- Built a FastAPI URL shortener service with endpoints for URL creation, redirect handling, health checks, and click analytics.
- Designed PostgreSQL models for short URL mappings and click events, including timestamps and simple request metadata.
- Integrated Redis caching for short-code lookups, with graceful fallback to PostgreSQL when the cache is unavailable.
- Added Docker Compose configuration to run the API, PostgreSQL, and Redis together in a repeatable local environment.

## Interview-Friendly Project Description

Built a backend URL shortener service that validates long URLs, generates unique short codes, redirects users to the original destination, and tracks click analytics. Used PostgreSQL as the permanent data store, Redis as a cache for faster redirects, FastAPI for REST endpoints and automatic API documentation, and Docker Compose to run the full stack locally.

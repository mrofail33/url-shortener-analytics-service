# Deployment and Operations Proof

Safe interview claim:

> I containerized a FastAPI backend with PostgreSQL and Redis dependencies and added CI tests for the core API behavior.

## Current proof

- `Dockerfile` builds the API service.
- `docker-compose.yml` starts API, PostgreSQL, and Redis together.
- `.github/workflows/ci.yml` runs the test suite on push and pull request.
- `docs/screenshots/openapi-docs.png` shows the API docs captured from a live local server.
- The test suite runs with SQLite so CI can verify behavior without external services.
- `docs/aws-deployment-cloudwatch.md` documents the AWS + CloudWatch path without adding Terraform or Kubernetes.

## Local verification commands

```bash
docker compose up --build
```

```bash
pytest
```

## What not to claim yet

- Do not claim a public production deployment.
- Do not claim production monitoring.
- Do not claim custom domain support.
- Do not claim migrations are complete.

## Simple next upgrade

Add Alembic migrations, a `/metrics` endpoint, and a short deployment log after pushing to a cloud host.

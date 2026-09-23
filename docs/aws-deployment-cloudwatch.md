# AWS Deployment and CloudWatch Proof

Safe interview claim:

> I prepared the URL shortener for an AWS container deployment path with GitHub Actions CI and CloudWatch logging notes.

## Final target architecture

```text
FastAPI + PostgreSQL + Redis + Docker
GitHub Actions -> AWS container deployment -> CloudWatch logs
```

## What is already in the repo

- `Dockerfile` builds the FastAPI service.
- `docker-compose.yml` runs the API with PostgreSQL and Redis locally.
- `.github/workflows/ci.yml` runs tests on every push and pull request.
- `/health` provides a simple health check for deployment platforms.
- The app reads configuration from environment variables.

## AWS deployment path

Keep the first AWS version simple:

1. Build the Docker image in GitHub Actions.
2. Push the image to Amazon ECR.
3. Run the container on ECS Fargate or App Runner.
4. Use managed PostgreSQL and Redis when moving beyond a lab.
5. Send container logs to CloudWatch Logs.
6. Add one CloudWatch alarm for repeated 5xx errors or unhealthy tasks.

## GitHub Actions secrets needed

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ECR_REPOSITORY
```

## What not to claim yet

- Do not claim Terraform.
- Do not claim Kubernetes.
- Do not claim production traffic.
- Do not claim autoscaling or advanced SRE.

## Simple interview wording

> The code is containerized and CI-tested. The next AWS step is to build the Docker image in GitHub Actions, push it to ECR, run it on a simple container service, and use CloudWatch for logs and basic alarms.

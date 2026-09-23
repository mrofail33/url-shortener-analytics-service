# AWS Deployment and CloudWatch Proof

Safe interview claim until the AWS secrets are connected:

> I prepared the URL shortener for an AWS container deployment path with GitHub Actions CI and CloudWatch logging notes.

Safe interview claim after `.github/workflows/aws-deploy.yml` runs successfully:

> I deployed the Dockerized FastAPI URL shortener to AWS App Runner from GitHub Actions and verified recent logs in CloudWatch.

## Final target architecture

```text
FastAPI + PostgreSQL + Redis + Docker
GitHub Actions -> AWS container deployment -> CloudWatch logs
```

## What is already in the repo

- `Dockerfile` builds the FastAPI service.
- `docker-compose.yml` runs the API with PostgreSQL and Redis locally.
- `.github/workflows/ci.yml` runs tests on every push and pull request.
- `.github/workflows/aws-deploy.yml` builds the Docker image, pushes it to ECR, updates App Runner, checks `/health`, and verifies recent CloudWatch logs.
- `scripts/verify_cloudwatch_logs.py` checks that CloudWatch has recent log events for the deployed service.
- `/health` provides a simple health check for deployment platforms.
- The app reads configuration from environment variables.

## AWS deployment path

Keep the first AWS version simple:

1. Create one ECR repository for the API image.
2. Create one App Runner service that uses an ECR image and port `8000`.
3. Add the GitHub secrets below.
4. Set the GitHub repository variable `ENABLE_AWS_DEPLOY` to `true`.
5. Run the `Deploy to AWS` workflow.
6. Confirm the workflow passes the health check and CloudWatch log check.

## GitHub Actions secrets needed

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ECR_REPOSITORY
AWS_APPRUNNER_SERVICE_ARN
AWS_APP_URL
CLOUDWATCH_LOG_GROUP
```

## Verification checklist

- GitHub Actions deploy workflow passes.
- `AWS_APP_URL/health` returns `{"status":"ok"}`.
- The deploy workflow prints recent CloudWatch log events.
- The app remains simple to explain: Docker image, App Runner service, health check, CloudWatch logs.

## What not to claim yet

- Do not claim Terraform.
- Do not claim Kubernetes.
- Do not claim production traffic.
- Do not claim autoscaling or advanced SRE.

## Simple interview wording

> The code is containerized and CI-tested. The AWS deploy workflow builds the Docker image, pushes it to ECR, updates App Runner, checks the health endpoint, and verifies CloudWatch logs.

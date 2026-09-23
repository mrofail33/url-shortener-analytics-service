# Security Notes

Safe interview claim:

> I handled basic API validation and failure behavior, and documented the security work that would be needed before production.

## Current proof

- FastAPI validates URL input through the request schema.
- Unknown short codes return a 404 instead of leaking backend errors.
- Redis failures are treated as cache failures, not source-of-truth failures.
- Tests cover invalid and missing short-code behavior.
- Configuration is environment-driven.

## What not to claim yet

- Do not claim malicious URL scanning.
- Do not claim abuse prevention.
- Do not claim private-network URL blocking.
- Do not claim user-level access control.

## Simple next upgrade

Add rate limiting and block unsafe destinations such as private IP ranges, `localhost`, and non-HTTP schemes.

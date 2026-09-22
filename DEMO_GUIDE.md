# Demo Guide

This is a simple 2-3 minute demo script.

## Option A: Docker Demo

Use this if Docker is installed.

Open PowerShell in the project folder:

```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\URL Shortener Interview Kit\url-shortener-analytics-service"
```

Create the environment file:

```powershell
copy .env.example .env
```

Start the app, database, and cache:

```powershell
docker compose up --build
```

Open the API docs:

```text
http://localhost:8000/docs
```

Stop the app when finished:

```powershell
docker compose down
```

## Option B: Local Demo Without Docker

Use this if Docker is not installed.

Open PowerShell in the project folder:

```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\URL Shortener Interview Kit\url-shortener-analytics-service"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Run the API with SQLite for a simple local demo:

```powershell
$env:DATABASE_URL='sqlite:///./local_demo.db'
$env:REDIS_URL='redis://localhost:6379/15'
$env:BASE_URL='http://localhost:8000'
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Note: In this local demo, Redis may not be running. That is okay because the app falls back to the database.

## 2-3 Minute Demo Sequence

### 1. Start With The Big Picture

Say:

"This is a backend URL shortener. It creates short links, redirects users to the original URLs, tracks clicks, stores data in PostgreSQL, and uses Redis to speed up repeated redirects."

### 2. Show The Health Check

In Swagger, open:

```text
GET /health
```

Click `Try it out`, then `Execute`.

Expected result:

```json
{
  "status": "ok"
}
```

Say:

"This confirms the API is running."

### 3. Create A Short URL

In Swagger, open:

```text
POST /api/urls
```

Use this request:

```json
{
  "original_url": "https://www.python.org"
}
```

Say:

"FastAPI validates the URL, the service generates a unique short code, and PostgreSQL saves the mapping."

Copy the returned `short_code`.

### 4. Test The Redirect

Open the returned `short_url` in the browser, or run:

```powershell
curl -i http://localhost:8000/YOUR_CODE_HERE
```

Say:

"On redirect, the app checks Redis first. If it misses, it loads from PostgreSQL, caches the result, records a click, and redirects."

### 5. Show Analytics

In Swagger, open:

```text
GET /api/urls/{short_code}/stats
```

Enter the short code and execute.

Say:

"This shows the click count and recent click metadata. Each successful redirect creates a click event in the database."

### 6. Close With Improvements

Say:

"If I continued improving this, I would add Alembic migrations, rate limiting, authentication for analytics, custom aliases, and better production monitoring."

## Run Tests

From the project folder:

```powershell
.\.venv\Scripts\python -m pytest
```

Expected result:

```text
4 passed
```

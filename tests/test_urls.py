import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/15"
os.environ["BASE_URL"] = "http://testserver"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import ClickEvent, ShortURL


test_engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_create_short_url():
    response = client.post("/api/urls", json={"original_url": "https://example.com/article"})

    assert response.status_code == 201
    data = response.json()
    assert data["original_url"].startswith("https://example.com/article")
    assert len(data["short_code"]) == 7
    assert data["short_url"] == f"http://testserver/{data['short_code']}"


def test_redirect_records_click_event():
    create_response = client.post("/api/urls", json={"original_url": "https://example.com/docs"})
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False,
        headers={"user-agent": "pytest", "referer": "https://referrer.test"},
    )

    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"].startswith("https://example.com/docs")

    db = TestingSessionLocal()
    try:
        saved_url = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
        click = db.query(ClickEvent).filter(ClickEvent.url_id == saved_url.id).first()
        assert click is not None
        assert click.user_agent == "pytest"
        assert click.referrer == "https://referrer.test"
    finally:
        db.close()


def test_stats_return_click_count():
    create_response = client.post("/api/urls", json={"original_url": "https://example.com/stats"})
    short_code = create_response.json()["short_code"]

    client.get(f"/{short_code}", follow_redirects=False)
    stats_response = client.get(f"/api/urls/{short_code}/stats")

    assert stats_response.status_code == 200
    data = stats_response.json()
    assert data["short_code"] == short_code
    assert data["click_count"] == 1
    assert len(data["recent_clicks"]) == 1


def test_missing_short_code_returns_404():
    response = client.get("/missing123", follow_redirects=False)

    assert response.status_code == 404

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine


settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="A beginner-friendly URL shortener with click analytics, PostgreSQL, Redis, and Docker.",
    )
    app.include_router(api_router)
    return app


Base.metadata.create_all(bind=engine)
app = create_app()

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.url import URLCreate, URLCreateResponse, URLStatsResponse
from app.services.urls import create_short_url, find_url_by_code, get_url_stats, record_click


router = APIRouter()
settings = get_settings()


def build_short_url(short_code: str) -> str:
    return f"{settings.base_url.rstrip('/')}/{short_code}"


@router.post("/api/urls", response_model=URLCreateResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    short_url = create_short_url(db, str(payload.original_url))

    return URLCreateResponse(
        id=short_url.id,
        original_url=short_url.original_url,
        short_code=short_url.short_code,
        short_url=build_short_url(short_url.short_code),
        created_at=short_url.created_at,
    )


@router.get("/api/urls/{short_code}/stats", response_model=URLStatsResponse)
def read_url_stats(short_code: str, db: Session = Depends(get_db)):
    stats = get_url_stats(db, short_code)
    if stats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    short_url, click_count, recent_clicks = stats
    return URLStatsResponse(
        id=short_url.id,
        original_url=short_url.original_url,
        short_code=short_url.short_code,
        short_url=build_short_url(short_url.short_code),
        created_at=short_url.created_at,
        click_count=click_count,
        recent_clicks=recent_clicks,
    )


@router.get("/{short_code}")
def redirect_to_original(short_code: str, request: Request, db: Session = Depends(get_db)):
    short_url = find_url_by_code(db, short_code)
    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    client_host = request.client.host if request.client else None
    record_click(
        db=db,
        short_url=short_url,
        ip_address=client_host,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer"),
    )

    return RedirectResponse(url=short_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

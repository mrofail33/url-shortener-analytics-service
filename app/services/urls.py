from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.click import ClickEvent
from app.models.url import ShortURL
from app.services.cache import get_cached_url, set_cached_url
from app.services.shortener import generate_unique_short_code


settings = get_settings()


def create_short_url(db: Session, original_url: str) -> ShortURL:
    short_url = ShortURL(
        original_url=original_url,
        short_code=generate_unique_short_code(db),
    )
    db.add(short_url)
    db.commit()
    db.refresh(short_url)
    return short_url


def find_url_by_code(db: Session, short_code: str) -> ShortURL | None:
    cached = get_cached_url(short_code)
    if cached:
        return ShortURL(
            id=cached["id"],
            short_code=cached["short_code"],
            original_url=cached["original_url"],
            created_at=cached["created_at"],
            is_active=cached["is_active"],
        )

    short_url = (
        db.query(ShortURL)
        .filter(ShortURL.short_code == short_code, ShortURL.is_active.is_(True))
        .first()
    )

    if short_url:
        set_cached_url(
            short_code,
            {
                "id": short_url.id,
                "short_code": short_url.short_code,
                "original_url": short_url.original_url,
                "created_at": short_url.created_at.isoformat(),
                "is_active": short_url.is_active,
            },
        )

    return short_url


def record_click(
    db: Session,
    short_url: ShortURL,
    ip_address: str | None,
    user_agent: str | None,
    referrer: str | None,
) -> ClickEvent:
    click = ClickEvent(
        url_id=short_url.id,
        ip_address=ip_address,
        user_agent=user_agent[:255] if user_agent else None,
        referrer=referrer[:500] if referrer else None,
    )
    db.add(click)
    db.commit()
    db.refresh(click)
    return click


def get_url_stats(db: Session, short_code: str) -> tuple[ShortURL, int, list[ClickEvent]] | None:
    short_url = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
    if short_url is None:
        return None

    click_count = (
        db.query(func.count(ClickEvent.id))
        .filter(ClickEvent.url_id == short_url.id)
        .scalar()
    )
    recent_clicks = (
        db.query(ClickEvent)
        .filter(ClickEvent.url_id == short_url.id)
        .order_by(ClickEvent.clicked_at.desc())
        .limit(10)
        .all()
    )
    return short_url, click_count or 0, recent_clicks

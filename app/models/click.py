from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ClickEvent(Base):
    __tablename__ = "click_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("short_urls.id"), index=True, nullable=False)
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    referrer: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    short_url = relationship("ShortURL", back_populates="clicks")

from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class URLCreate(BaseModel):
    original_url: AnyHttpUrl = Field(..., examples=["https://example.com/articles/fastapi"])


class URLCreateResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClickEventResponse(BaseModel):
    clicked_at: datetime
    ip_address: str | None
    user_agent: str | None
    referrer: str | None

    model_config = ConfigDict(from_attributes=True)


class URLStatsResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int
    recent_clicks: list[ClickEventResponse]

    model_config = ConfigDict(from_attributes=True)

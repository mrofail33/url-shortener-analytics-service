import secrets
import string

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.url import ShortURL


settings = get_settings()
ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int | None = None) -> str:
    code_length = length or settings.short_code_length
    return "".join(secrets.choice(ALPHABET) for _ in range(code_length))


def generate_unique_short_code(db: Session) -> str:
    while True:
        short_code = generate_short_code()
        existing = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
        if existing is None:
            return short_code

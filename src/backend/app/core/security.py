from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from app.core.config import settings
from app.core.models.token_blacklist import TokenBlacklist, TokenType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def is_token_blacklisted(session: Session, token: str) -> bool:
    blacklisted = session.query(TokenBlacklist).filter(
        TokenBlacklist.token == token,
        TokenBlacklist.expires_at > datetime.now(timezone.utc)
    ).first()
    return blacklisted is not None


def blacklist_token(
    session: Session,
    token: str,
    token_type: TokenType,
    expires_at: datetime,
    blacklisted_by: int | None = None
) -> TokenBlacklist:
    token_entry = TokenBlacklist(
        token=token,
        token_type=token_type,
        expires_at=expires_at,
        blacklisted_by=blacklisted_by
    )
    session.add(token_entry)
    session.commit()
    session.refresh(token_entry)
    return token_entry

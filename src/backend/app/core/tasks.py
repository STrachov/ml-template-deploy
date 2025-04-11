from datetime import datetime, timezone
from sqlmodel import Session, select
from app.core.models.token_blacklist import TokenBlacklist

def cleanup_expired_tokens(session: Session) -> int:
    """
    Remove expired tokens from the blacklist
    Returns the number of tokens removed
    """
    stmt = select(TokenBlacklist).where(TokenBlacklist.expires_at < datetime.now(timezone.utc))
    expired_tokens = session.exec(stmt).all()
    for token in expired_tokens:
        session.delete(token)
    session.commit()
    return len(expired_tokens)

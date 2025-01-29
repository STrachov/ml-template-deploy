import uuid

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class RefreshToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    refresh_token: str = Field(nullable=False, unique=True)
    expires_at: datetime = Field(nullable=False)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    revoked: bool = Field(default=False)

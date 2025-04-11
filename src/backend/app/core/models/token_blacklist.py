from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class TokenBlacklist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str = Field(index=True)
    token_type: TokenType = Field(index=True)
    blacklisted_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    blacklisted_by: uuid.UUID = Field(foreign_key="user.id", nullable=True)

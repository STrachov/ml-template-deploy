# from __future__ import annotations  # Enables forward references in type hints

import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy.orm import relationship

# from app.core.models.user import User
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class ActionBase(SQLModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(min_length=1, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prompt: str = Field(min_length=50)
    output: str = Field(min_length=50)
    cost: float = Field(default=0.0, ge=0.0)


# Properties to receive on item creation
class ActionCreate(ActionBase):
    pass


# Properties to receive on item update
class ActionUpdate(ActionBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Action(ActionBase, table=True):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="actions")


# Properties to return via API, id is always required
class ActionPublic(ActionBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ActionsPublic(SQLModel):
    data: list[ActionPublic]
    count: int

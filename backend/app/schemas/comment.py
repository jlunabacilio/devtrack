from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserRead


class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    issue_id: int


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    issue_id: int
    author: UserRead
    created_at: datetime

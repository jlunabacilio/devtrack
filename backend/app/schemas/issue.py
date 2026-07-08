from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.base import IssuePriority, IssueStatus
from app.schemas.user import UserRead


class IssueBase(BaseModel):
    title: str
    description: str | None = None
    status: IssueStatus = IssueStatus.open
    priority: IssuePriority = IssuePriority.medium
    project_id: int
    assignee_id: int | None = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    """All fields optional — supports PATCH semantics."""
    title: str | None = None
    description: str | None = None
    status: IssueStatus | None = None
    priority: IssuePriority | None = None
    assignee_id: int | None = None


class IssueStatusUpdate(BaseModel):
    """Dedicated payload for the PATCH /issues/{id}/status endpoint."""
    status: IssueStatus


class IssueRead(IssueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    assignee: UserRead | None = None

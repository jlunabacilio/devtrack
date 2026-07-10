from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

IssueStatus = Literal["open", "in_progress", "closed"]


class IssueBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: IssueStatus | None = None


class IssueRead(IssueBase):
    id: int
    status: IssueStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

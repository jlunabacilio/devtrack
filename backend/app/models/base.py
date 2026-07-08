import enum

from sqlalchemy import DateTime, func
from sqlalchemy.orm import MappedColumn, mapped_column


# ---------------------------------------------------------------------------
# Enums — stored as VARCHAR so they're portable across any SQL engine
# ---------------------------------------------------------------------------

class UserRole(str, enum.Enum):
    admin = "admin"
    member = "member"


class IssueStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class IssuePriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


# ---------------------------------------------------------------------------
# Mixin — adds created_at / updated_at to any model that inherits it
# ---------------------------------------------------------------------------

class TimestampMixin:
    created_at: MappedColumn[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: MappedColumn[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import IssuePriority, IssueStatus, TimestampMixin

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.project import Project
    from app.models.user import User


class Issue(TimestampMixin, Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[IssueStatus] = mapped_column(
        Enum(IssueStatus, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=IssueStatus.open,
    )
    priority: Mapped[IssuePriority] = mapped_column(
        Enum(IssuePriority, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=IssuePriority.medium,
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assignee_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="issues")
    assignee: Mapped["User | None"] = relationship(
        "User", back_populates="issues_assigned", foreign_keys=[assignee_id]
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="issue", cascade="all, delete-orphan"
    )

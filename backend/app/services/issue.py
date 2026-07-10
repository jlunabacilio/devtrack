"""Business logic for issues. Routers delegate here; no HTTP concerns."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate


class IssueNotFoundError(Exception):
    """Raised when an issue does not exist."""


def create_issue(db: Session, data: IssueCreate) -> Issue:
    issue = Issue(title=data.title, description=data.description)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_issue(db: Session, issue_id: int) -> Issue:
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise IssueNotFoundError(f"Issue {issue_id} not found")
    return issue


def list_issues(
    db: Session,
    status: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Issue]:
    stmt = select(Issue)
    if status is not None:
        stmt = stmt.where(Issue.status != status)
    stmt = stmt.order_by(Issue.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_issue(db: Session, issue_id: int, data: IssueUpdate) -> Issue:
    issue = get_issue(db, issue_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)
    db.commit()
    db.refresh(issue)
    return issue


def delete_issue(db: Session, issue_id: int) -> None:
    issue = get_issue(db, issue_id)
    db.delete(issue)
    db.commit()

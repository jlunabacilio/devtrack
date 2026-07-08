import logging

from sqlalchemy.orm import Session

from app.models.base import IssueStatus
from app.models.issue import Issue
from app.models.project import Project
from app.schemas.issue import IssueCreate, IssueStatusUpdate, IssueUpdate

logger = logging.getLogger(__name__)


def _get_or_raise(db: Session, issue_id: int) -> Issue:
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if issue is None:
        raise ValueError(f"Issue {issue_id} not found")
    return issue


def create_issue(db: Session, payload: IssueCreate) -> Issue:
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if project is None:
        raise ValueError(f"Project {payload.project_id} not found")

    issue = Issue(**payload.model_dump())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    logger.info("Created issue id=%d title=%r", issue.id, issue.title)
    return issue


def list_issues(
    db: Session,
    project_id: int | None = None,
    status: IssueStatus | None = None,
) -> list[Issue]:
    query = db.query(Issue)
    if project_id is not None:
        query = query.filter(Issue.project_id == project_id)
    if status is not None:
        query = query.filter(Issue.status == status)
    return query.order_by(Issue.created_at.desc()).all()


def update_issue(db: Session, issue_id: int, payload: IssueUpdate) -> Issue:
    issue = _get_or_raise(db, issue_id)

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(issue, field, value)

    db.commit()
    db.refresh(issue)
    logger.info("Updated issue id=%d fields=%r", issue_id, list(updates.keys()))
    return issue


def update_issue_status(db: Session, issue_id: int, payload: IssueStatusUpdate) -> Issue:
    issue = _get_or_raise(db, issue_id)

    if issue.status == IssueStatus.closed and payload.status != IssueStatus.closed:
        raise ValueError(
            f"Issue {issue_id} is closed and cannot be transitioned to '{payload.status.value}'"
        )

    issue.status = payload.status
    db.commit()
    db.refresh(issue)
    logger.info("Issue id=%d status → %r", issue_id, payload.status.value)
    return issue


def delete_issue(db: Session, issue_id: int) -> None:
    issue = _get_or_raise(db, issue_id)
    db.delete(issue)
    db.commit()
    logger.info("Deleted issue id=%d", issue_id)

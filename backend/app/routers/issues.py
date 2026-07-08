import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base import IssueStatus
from app.schemas.issue import IssueCreate, IssueRead, IssueStatusUpdate, IssueUpdate
from app.services import issue as issue_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post(
    "",
    response_model=IssueRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new issue",
)
def create_issue(payload: IssueCreate, db: Session = Depends(get_db)) -> IssueRead:
    try:
        return issue_service.create_issue(db, payload)
    except ValueError as exc:
        logger.warning("create_issue rejected: %s", exc)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


@router.get(
    "",
    response_model=list[IssueRead],
    summary="List issues, optionally filtered by project and/or status",
)
def list_issues(
    project_id: int | None = Query(default=None, description="Filter by project ID"),
    status: IssueStatus | None = Query(default=None, description="Filter by status"),
    db: Session = Depends(get_db),
) -> list[IssueRead]:
    return issue_service.list_issues(db, project_id=project_id, status=status)


@router.patch(
    "/{issue_id}",
    response_model=IssueRead,
    summary="Partially update an issue (title, description, priority, assignee, status)",
)
def update_issue(
    issue_id: int, payload: IssueUpdate, db: Session = Depends(get_db)
) -> IssueRead:
    try:
        return issue_service.update_issue(db, issue_id, payload)
    except ValueError as exc:
        logger.warning("update_issue id=%d: %s", issue_id, exc)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch(
    "/{issue_id}/status",
    response_model=IssueRead,
    summary="Update an issue's status",
)
def update_issue_status(
    issue_id: int, payload: IssueStatusUpdate, db: Session = Depends(get_db)
) -> IssueRead:
    try:
        return issue_service.update_issue_status(db, issue_id, payload)
    except ValueError as exc:
        logger.warning("update_issue_status id=%d: %s", issue_id, exc)
        detail = str(exc)
        code = (
            status.HTTP_409_CONFLICT
            if "closed" in detail
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=code, detail=detail)


@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an issue",
)
def delete_issue(issue_id: int, db: Session = Depends(get_db)) -> None:
    try:
        issue_service.delete_issue(db, issue_id)
    except ValueError as exc:
        logger.warning("delete_issue id=%d: %s", issue_id, exc)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

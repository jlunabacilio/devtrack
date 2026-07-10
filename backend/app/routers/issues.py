"""HTTP routes for issues. Delegates all logic to app.services.issue."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.issue import IssueCreate, IssueRead, IssueStatus, IssueUpdate
from app.services import issue as issue_service

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate, db: Session = Depends(get_db)) -> IssueRead:
    return issue_service.create_issue(db, payload)


@router.get("", response_model=list[IssueRead])
def list_issues(
    status_filter: IssueStatus | None = Query(default=None, alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[IssueRead]:
    return issue_service.list_issues(db, status=status_filter, skip=skip, limit=limit)


@router.get("/{issue_id}", response_model=IssueRead)
def get_issue(issue_id: int, db: Session = Depends(get_db)) -> IssueRead:
    try:
        return issue_service.get_issue(db, issue_id)
    except issue_service.IssueNotFoundError:
        raise HTTPException(status_code=404, detail="Issue not found")


@router.patch("/{issue_id}", response_model=IssueRead)
def update_issue(
    issue_id: int, payload: IssueUpdate, db: Session = Depends(get_db)
) -> IssueRead:
    try:
        return issue_service.update_issue(db, issue_id, payload)
    except issue_service.IssueNotFoundError:
        raise HTTPException(status_code=404, detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: int, db: Session = Depends(get_db)) -> None:
    try:
        issue_service.delete_issue(db, issue_id)
    except issue_service.IssueNotFoundError:
        raise HTTPException(status_code=404, detail="Issue not found")

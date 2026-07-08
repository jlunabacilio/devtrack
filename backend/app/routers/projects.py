import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectRead
from app.services import project as project_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    try:
        return project_service.create_project(db, payload)
    except ValueError as exc:
        logger.warning("create_project rejected: %s", exc)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get(
    "",
    response_model=list[ProjectRead],
    summary="List all projects",
)
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    return project_service.list_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get a project by ID",
)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    try:
        return project_service.get_project(db, project_id)
    except ValueError as exc:
        logger.warning("get_project id=%d: %s", project_id, exc)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

import logging

from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate

logger = logging.getLogger(__name__)


def create_project(db: Session, payload: ProjectCreate) -> Project:
    existing = db.query(Project).filter(Project.name == payload.name).first()
    if existing:
        raise ValueError(f"A project named '{payload.name}' already exists")

    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    logger.info("Created project id=%d name=%r", project.id, project.name)
    return project


def list_projects(db: Session) -> list[Project]:
    return db.query(Project).order_by(Project.name).all()


def get_project(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise ValueError(f"Project {project_id} not found")
    return project

# Import every model here so that SQLAlchemy's Base.metadata and
# Alembic's autogenerate both see all tables at startup.
from app.models.comment import Comment
from app.models.issue import Issue
from app.models.project import Project
from app.models.user import User

__all__ = ["User", "Project", "Issue", "Comment"]

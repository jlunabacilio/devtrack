# FastAPI APIRouter instances live here.
# Each module groups endpoints for one resource (e.g. issues, users).
# Routers are registered in app/main.py via app.include_router().
from app.routers import issues, projects

__all__ = ["projects", "issues"]

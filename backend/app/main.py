from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routers import issues, projects

app = FastAPI(
    title="DevTrack API",
    version="0.1.0",
    # RFC 7807-style error shape: {"detail": "...", "type": "..."}
    responses={422: {"description": "Validation error"}},
)

app.include_router(projects.router, prefix="/api/v1")
app.include_router(issues.router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "type": "validation_error"},
    )


@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok"}

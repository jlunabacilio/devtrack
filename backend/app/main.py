from fastapi import FastAPI

from app.routers import issues

app = FastAPI(title="DevTrack API", version="0.1.0")

app.include_router(issues.router)


@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok"}

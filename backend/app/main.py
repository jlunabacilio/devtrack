from fastapi import FastAPI

app = FastAPI(title="DevTrack API", version="0.1.0")


@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok"}

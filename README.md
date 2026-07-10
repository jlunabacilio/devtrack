# DevTrack

A lightweight issue tracker built with **FastAPI** (Python 3.12) on the backend and **React 18 + TypeScript** on the frontend.

---

## Prerequisites

| Tool | Minimum version |
|---|---|
| Python | 3.12 |
| Node.js | 20 LTS |
| npm | 10 |

---

## Project structure

```
devtrack/
├── backend/   # FastAPI · SQLAlchemy · SQLite · Alembic
└── frontend/  # React 18 · TypeScript · Vite
```

---

## Getting started

### 1 — Clone the repo

```bash
git clone <repo-url> devtrack
cd devtrack
```

### 2 — Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install runtime + dev dependencies
pip install -e ".[dev]"

# Create your local environment file
cp .env.example .env             # edit DATABASE_URL if needed

# Start the API (reloads on file changes)
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`.

### 3 — Frontend setup

```bash
cd frontend

npm install

# Start the dev server (proxies /api → localhost:8000)
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## Available commands

### Backend

| Command | Description |
|---|---|
| `uvicorn app.main:app --reload` | Run dev server |
| `pytest` | Run test suite |
| `ruff check .` | Lint |
| `mypy app` | Type-check |

### Frontend

| Command | Description |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run lint` | ESLint |
| `npm run type-check` | TypeScript check |

---

## Environment variables

Copy `backend/.env.example` to `backend/.env` and adjust as needed.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./devtrack.db` | SQLAlchemy connection string |
| `ENVIRONMENT` | `development` | `development` or `production` |

> **Never commit `.env` to version control.**

---

## Contributing

1. Branch off `main`: `git checkout -b feat/<short-description>`
2. Keep cognitive complexity ≤ 15 and test coverage ≥ 80 % (SonarQube gate).
3. Open a pull request — CI must be green before merging.

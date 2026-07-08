# GitHub Copilot Instructions — DevTrack

## Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.x (ORM only), SQLite, Alembic, Pydantic v2
- **Frontend**: TypeScript strict mode, React 18, Vite, React hooks only (no class components)
- **Testing**: Pytest + pytest-asyncio (backend), Vitest + Testing Library (frontend)
- **Quality gate**: SonarQube — keep cognitive complexity ≤ 15, coverage ≥ 80 %

## Naming Conventions
- Python: `snake_case` for files, functions, variables; `PascalCase` for classes and Pydantic models
- TypeScript: `camelCase` for variables/functions; `PascalCase` for components, interfaces, and types
- Database columns: `snake_case`; boolean columns prefixed `is_` or `has_`
- React components: one component per file, filename matches component name

## Folder Structure (do not deviate)
- `backend/app/models/` — SQLAlchemy ORM models only
- `backend/app/schemas/` — Pydantic request/response schemas only
- `backend/app/routers/` — FastAPI route handlers; delegate logic to services
- `backend/app/services/` — all business logic; no HTTP concerns
- `frontend/src/components/` — reusable UI; `frontend/src/pages/` — route-level views
- `frontend/src/services/` — API client calls; `frontend/src/hooks/` — custom hooks

## Error Handling
- Backend: raise `HTTPException` in routers; raise domain `ValueError` / custom exceptions in services
- Never swallow exceptions silently; always log with context before re-raising
- Frontend: wrap API calls in try/catch; surface errors through a dedicated error state, never `console.error` only
- Return RFC 7807 Problem Details shape: `{ detail: string, type: string }`

## Security Rules — always enforced, no exceptions
1. **Never concatenate raw strings into SQL.** Use SQLAlchemy ORM or parameterized `text()` with bound params only.
2. **Never hardcode secrets, tokens, or credentials.** All secrets come from environment variables via `pydantic-settings` (backend) or `import.meta.env` (frontend).
3. **Always validate resource-level authorization** before returning or mutating data (verify the requesting user owns or has permission on the resource).
4. **Always sanitize and validate all external input** at the schema/Pydantic layer; never trust raw request data in services.
5. **Never expose internal error details** (stack traces, SQL errors) in API responses.
6. **Dependencies**: do not introduce new packages without checking for known CVEs (`pip audit` / `npm audit`).

# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

LaundroMate is a pnpm monorepo with a FastAPI backend (`apps/api`) and Next.js frontend (`apps/web`), plus shared packages (`packages/ui`, `packages/types`, `packages/utils`).

### Services

| Service | Port | Command |
|---------|------|---------|
| PostgreSQL 15 | 5433 (host) → 5432 (container) | `docker compose up -d postgres` (from repo root) |
| FastAPI API | 8000 | `python3 -m uvicorn app.main:app --reload` (from `apps/api`) |
| Next.js Web | 3000 | `pnpm dev` (from `apps/web`) |

### Starting services

1. Start Docker daemon if not running: `sudo dockerd &>/tmp/dockerd.log &` then `sudo chmod 666 /var/run/docker.sock`
2. Start PostgreSQL: `docker compose up -d postgres` (from repo root)
3. The API `.env` must use port **5433** for `DATABASE_URL` (e.g. `postgresql://laundromate:laundromate@localhost:5433/laundromate`) because docker-compose maps 5433→5432.
4. Start API: `cd apps/api && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
5. Build UI package before starting web: `pnpm --filter @laundromate/ui build`
6. Start frontend: `cd apps/web && pnpm dev`

### Key gotchas

- **`alembic` CLI not on PATH**: Use `python3 -m alembic` instead of bare `alembic`.
- **Migration bug in `b2c3d4e5f6a7`**: The last migration creates a `userorganizationrole` enum type both implicitly (via `sa.Enum` in `create_table`) and explicitly (via `CREATE TYPE`). On a fresh DB, run `python3 -m alembic upgrade a1b2c3d4e5f6` first, then manually apply the remaining SQL (creating the enum, table, and columns) and stamp `UPDATE alembic_version SET version_num = 'b2c3d4e5f6a7'`.
- **`.env` extra fields**: The `Settings` class in `app/core/config/settings.py` does **not** allow extra fields. The `.env.example` contains fields not in the Settings model (`REDIS_URL`, `DEBUG`, `TWILIO_*`, `SMTP_*`). When creating `.env`, only include fields defined in the `Settings` class, or pydantic-settings will reject them.
- **`verification_codes` table missing from migrations**: The `VerificationCode` model exists but no migration creates its table. Create it manually in PostgreSQL if testing the OTP auth flow.
- **Test suite uses SQLite**: The test `conftest.py` uses SQLite, but models use PostgreSQL-specific types (e.g. `ARRAY`). Most database-dependent tests will error. Pure domain logic tests pass.
- **passlib/bcrypt compatibility**: `passlib` has a known incompatibility with newer `bcrypt` versions. Password hashing tests fail. Use `bcrypt.hashpw()` directly if you need to hash passwords outside the running app.

### Lint & Test commands

- **Frontend lint**: `pnpm --filter @laundromate/web lint` (runs `next lint`)
- **Backend lint**: `cd apps/api && python3 -m flake8 app/ --max-line-length=88`
- **Backend tests**: `cd apps/api && python3 -m pytest tests/unit/domain/ -v` (domain tests only; DB-dependent tests fail due to SQLite/PostgreSQL mismatch)
- **Formatting**: `cd apps/api && python3 -m black . && python3 -m isort .`

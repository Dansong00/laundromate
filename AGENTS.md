# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

LaundroMate is a pnpm monorepo with a FastAPI backend (`apps/api`) and a Next.js 14 frontend (`apps/web`), plus three shared TypeScript packages (`packages/ui`, `packages/types`, `packages/utils`). PostgreSQL 15 is required infrastructure.

### Services

| Service | Port | How to start |
|---------|------|-------------|
| PostgreSQL | 5433 (mapped to 5432 inside container) | `docker compose up -d postgres` from repo root |
| FastAPI API | 8000 | `cd apps/api && source .venv/bin/activate && PYTHONPATH=$PWD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| Next.js Web | 3000 | `pnpm --filter @laundromate/web dev` from repo root |

### Lint / Test / Build

See `package.json` scripts in root and `apps/web/package.json`, plus `pyproject.toml` in `apps/api`.

- **API lint**: `cd apps/api && source .venv/bin/activate && flake8 --config .flake8 app/`
- **API tests**: `cd apps/api && source .venv/bin/activate && PYTHONPATH=$PWD pytest`
- **Web lint**: `pnpm --filter @laundromate/web lint`
- **Web tests**: `cd apps/web && npx vitest --run`
- **Web build**: `pnpm --filter @laundromate/web build`

### Non-obvious caveats

- **Database port**: Docker maps PostgreSQL to **port 5433** on the host (not 5432). The `.env` file in `apps/api` must use port **5433** in the `DATABASE_URL`. Copy `.env.example` and update the port from 5432 to 5433.
- **Alembic**: `alembic.ini` hard-codes the DB URL pointing to `postgres:5432` (Docker network hostname). For local development, alembic reads the URL from `app.core.database.session.engine`, which loads from `.env`. Always run alembic from `apps/api` with the venv activated and `PYTHONPATH` set.
- **Settings strict mode**: `app.core.config.settings.Settings` (pydantic-settings) forbids extra fields. The `.env` file must only contain fields declared in the Settings model (no `REDIS_URL`, `DEBUG`, `TWILIO_*` etc.).
- **bcrypt compatibility**: passlib 1.7.4 is incompatible with bcrypt >= 4.1. Pin `bcrypt==4.0.1` in the venv to avoid `AttributeError: module 'bcrypt' has no attribute '__about__'`.
- **Pytest ARRAY errors**: ~306 test errors are pre-existing — tests use SQLite which doesn't support PostgreSQL ARRAY columns. The 75 passing tests and 17 failures are the real test results.
- **Docker in Cloud VM**: Docker daemon must be started with `sudo dockerd` and `fuse-overlayfs` storage driver. The socket needs `chmod 666 /var/run/docker.sock` for non-root access.
- **pnpm build scripts**: On first `pnpm install`, some packages (`@clerk/shared`, `esbuild`, `unrs-resolver`) have blocked build scripts. These do not affect dev functionality.

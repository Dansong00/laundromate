# LaundroMate Dev Container

This dev container provides a consistent development environment for the LaundroMate project.

## Features

- **Python 3.11** with Poetry package management
- **Docker socket access** for running docker-compose commands
- **Pre-installed extensions** for Python development
- **Code formatting** with Black, isort, and flake8
- **Port forwarding** for API (8000), PostgreSQL (5432), and Redis (6379)

## Getting Started

1. **Install the Dev Containers extension** in Cursor/VS Code
2. **Open the project** in Cursor
3. **When prompted**, click "Reopen in Container"
4. **Wait for the container to build** and start

## What Happens

- Cursor will run inside the Python container
- All Python dependencies will be available
- Import resolution errors will disappear
- You can run `docker compose up` from inside the container

## Development Workflow

1. **Edit code** in Cursor (running in container)
2. **Install dependencies**: `poetry install` (in `/workspace/apps/api`)
3. **Run your app**: `docker compose up` (from container)
4. **All imports resolve correctly** - no more "could not be resolved" errors!

## Ports

- **8000**: FastAPI application
- **5432**: PostgreSQL database
- **6379**: Redis cache

## Troubleshooting

If you encounter issues:
1. **Rebuild container**: Command Palette → "Dev Containers: Rebuild Container"
2. **Check Docker**: Ensure Docker Desktop is running on your host
3. **Verify ports**: Check if ports 8000, 5432, 6379 are available
4. **Clear cache**: Delete `.devcontainer` folder and recreate if needed

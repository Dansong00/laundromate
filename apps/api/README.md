# LaundroMate API

FastAPI backend for the LaundroMate SaaS platform - a modern solution for full-service laundromats.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Poetry (recommended) or pip

### Setup Steps

1. **Install dependencies**
   ```bash
   poetry install
   # or
   pip install -r requirements.txt
   ```

2. **Start database services**
   ```bash
   docker compose up -d postgres redis
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

4. **Create database**
   ```bash
   docker compose exec postgres psql -U laundromate -c "CREATE DATABASE laundromate;"
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the API**
   ```bash
   poetry run uvicorn app.main:app --reload
   # or
   uvicorn app.main:app --reload
   ```

## 🗄️ Database Management

### Running Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Rollback one migration
alembic downgrade -1

# Check current status
alembic current

# View migration history
alembic history
```

### Development vs Production
- **Development**: Use `alembic upgrade head` to get latest schema
- **Production**: Run migrations as part of deployment process

## ��️ Project Structure

```
app/
├── auth/           # Authentication & authorization
├── core/           # Core configuration & database
├── customers/      # Customer management
├── orders/         # Order processing
└── notifications/  # Email/SMS notifications
```

## 🔧 Development

### Running Tests
```bash
poetry run pytest
# or
pytest
```

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

### Linting
```bash
poetry run flake8
```

## 🐳 Docker Development

### Start all services
```bash
docker compose up -d
```

### View logs
```bash
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redis
```

### Rebuild API
```bash
docker compose build api
docker compose up -d api
```

## 🚨 Troubleshooting

### Common Issues

1. **Database connection failed**
   - Ensure PostgreSQL is running: `docker compose ps postgres`
   - Check DATABASE_URL in .env file
   - Verify database exists: `docker compose exec postgres psql -U laundromate -l`

2. **Port already in use**
   - Stop local PostgreSQL/Redis: `brew services stop postgresql` (macOS)
   - Or change ports in docker-compose.yml

3. **Migration errors**
   - Check alembic/env.py configuration
   - Ensure all models are imported in app/core/models/__init__.py

4. **Import errors**
   - Verify Python path includes app directory
   - Check __init__.py files exist in all packages

### Getting Help

- Check the logs: `docker compose logs api`
- Verify environment variables: `docker compose exec api env | grep DATABASE`
- Test database connection: `docker compose exec api python -c "from app.core.database.session import engine; print(engine.url)"`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://laundromate:laundromate@localhost:5432/laundromate` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `ENV` | Environment (development/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Create a pull request

## 📄 License

This project is proprietary software.

# 🚀 Quick Setup Guide for New Developers

This guide will get you up and running with LaundroMate API in under 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd LaundroMate/apps/api

# 2. Install dependencies
pip install -e .[dev]
# or: pip install .

# 3. Start database
docker compose up -d postgres redis

# 4. Setup database (one command!)
./scripts/init-db.sh

# 5. Start API
uvicorn app.main:app --reload
```

## 🎯 What Just Happened?

The `init-db.sh` script automatically:

- ✅ Starts PostgreSQL if needed
- ✅ Creates the database if it doesn't exist
- ✅ Runs all pending migrations
- ✅ Sets up the complete schema

## 🌐 Verify Everything Works

- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Root Endpoint**: http://localhost:8000/

## 🚨 If Something Goes Wrong

1. **Check Docker**: `docker compose ps`
2. **View Logs**: `docker compose logs api`
3. **Restart Services**: `docker compose restart`
4. **Ask for Help**: Check the main README.md for troubleshooting

## 🔄 Daily Development

```bash
# Start services
docker compose up -d

# Start API
poetry run uvicorn app.main:app --reload

# Stop everything
docker compose down
```

## 📚 Next Steps

- Read the main README.md for detailed information
- Check out the API documentation at /docs
- Explore the codebase structure
- Join team discussions!

---

**Need help?** Check the main README.md or ask the team!

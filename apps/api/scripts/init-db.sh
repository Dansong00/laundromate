#!/bin/bash

echo "🚀 Initializing LaundroMate database..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] && [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the apps/api directory"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if postgres service is running
if ! docker compose ps postgres | grep -q "Up"; then
    echo "�� Starting PostgreSQL service..."
    docker compose up -d postgres
    sleep 5
fi

# Check if database exists
echo "🔍 Checking if database exists..."
DB_EXISTS=$(docker compose exec -T postgres psql -U laundromate -lqt 2>/dev/null | grep -c laundromate)

if [ $DB_EXISTS -gt 0 ]; then
    echo "✅ Database 'laundromate' already exists"
else
    echo "📝 Creating database 'laundromate'..."
    docker compose exec -T postgres psql -U laundromate -c "CREATE DATABASE laundromate;" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Database created successfully"
    else
        echo "❌ Failed to create database. Please check PostgreSQL logs:"
        echo "   docker compose logs postgres"
        exit 1
    fi
fi

# Check if alembic is configured
if [ ! -f "alembic.ini" ]; then
    echo "❌ Error: alembic.ini not found. Please run 'alembic init alembic' first."
    exit 1
fi

# Run migrations
echo "🔧 Running database migrations..."

# Try to run with Poetry first, then with pip
if command -v poetry >/dev/null 2>&1; then
    echo "📦 Using Poetry to run migrations..."
    poetry run alembic upgrade head
    MIGRATION_SUCCESS=$?
else
    echo "📦 Poetry not found, trying direct alembic..."
    alembic upgrade head
    MIGRATION_SUCCESS=$?
fi

if [ $MIGRATION_SUCCESS -eq 0 ]; then
    echo "✅ Database setup complete!"
    echo ""
    echo "🎉 You can now start the API with:"
    if command -v poetry >/dev/null 2>&1; then
        echo "   poetry run uvicorn app.main:app --reload"
    fi
    echo "   uvicorn app.main:app --reload"
else
    echo "❌ Migration failed. Please check the error messages above."
    echo ""
    echo "💡 Try running manually:"
    if command -v poetry >/dev/null 2>&1; then
        echo "   poetry run alembic upgrade head"
    else
        echo "   alembic upgrade head"
    fi
    exit 1
fi

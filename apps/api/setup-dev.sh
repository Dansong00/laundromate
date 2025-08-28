#!/bin/bash

echo "🚀 Setting up LaundroMate API development environment..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the apps/api directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -e .[dev]

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start database services
echo "🗄️ Starting database services..."
docker compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Run database initialization
echo "🔧 Setting up database..."
./scripts/init-db.sh

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Development environment setup complete!"
    echo ""
    echo "🚀 Start the API with:"
    echo "   uvicorn app.main:app --reload"
    echo ""
    echo "📚 API documentation will be available at:"
    echo "   http://localhost:8000/docs"
else
    echo "❌ Database setup failed. Please check the error messages above."
    exit 1
fi

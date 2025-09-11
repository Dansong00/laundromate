#!/bin/bash

# LaundroMate API Test Environment Setup Script

set -e

echo "🧪 Setting up LaundroMate API test environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install --break-system-packages pytest pytest-cov pytest-asyncio pytest-httpx factory-boy faker httpx black isort flake8 mypy

# Create test database directory if it doesn't exist
mkdir -p /tmp/laundromate_test_db

# Run existing tests to verify setup
echo "🧪 Running existing tests to verify setup..."
python3 -m pytest tests/ -v --tb=short

echo "✅ Test environment setup complete!"
echo ""
echo "📋 Available test commands:"
echo "  python3 -m pytest tests/                    # Run all tests"
echo "  python3 -m pytest tests/ -v                 # Run with verbose output"
echo "  python3 -m pytest tests/ --cov=app         # Run with coverage"
echo "  python3 -m pytest tests/ -k 'auth'          # Run only auth tests"
echo "  python3 -m pytest tests/ --cov=app --cov-report=html  # Generate HTML coverage report"
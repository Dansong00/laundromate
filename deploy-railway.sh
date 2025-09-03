#!/bin/bash

echo "🚂 Deploying LaundroMate to Railway"
echo "===================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI already installed"
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please log in to Railway..."
    railway login
else
    echo "✅ Already logged in to Railway"
fi

# Check if project is linked
if [ ! -f ".railway/project.json" ]; then
    echo "🔗 Linking project to Railway..."
    railway link
else
    echo "✅ Project already linked to Railway"
fi

# Deploy all services
echo "🚀 Deploying services to Railway..."
railway up

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Your services are now available at:"
echo "🌐 Frontend: https://your-project-name.railway.app"
echo "🔌 API: https://your-api-service.railway.app"
echo "🗄️  Database: Managed by Railway"
echo "🔴 Redis: Managed by Railway"
echo ""
echo "To view logs: railway logs"
echo "To open dashboard: railway open"


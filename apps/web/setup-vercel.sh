#!/bin/bash

echo "🚀 Setting up Vercel deployment for LaundroMate Frontend"
echo "========================================================"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
else
    echo "✅ Vercel CLI already installed"
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
else
    echo "✅ Already logged in to Vercel"
fi

# Link project if not already linked
if [ ! -f ".vercel/project.json" ]; then
    echo "🔗 Linking project to Vercel..."
    vercel link
else
    echo "✅ Project already linked to Vercel"
fi

# Set up environment variables
echo "🌍 Setting up environment variables..."
echo "Please configure the following in your Vercel dashboard:"
echo ""
echo "For Staging:"
echo "  NEXT_PUBLIC_API_URL=https://your-staging-api.railway.app"
echo "  NEXT_PUBLIC_APP_ENVIRONMENT=staging"
echo ""
echo "For Production:"
echo "  NEXT_PUBLIC_API_URL=https://your-production-api.railway.app"
echo "  NEXT_PUBLIC_APP_ENVIRONMENT=production"
echo ""

# Test build
echo "🔨 Testing build..."
if pnpm build; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo ""
echo "🎉 Vercel setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure environment variables in Vercel dashboard"
echo "2. Deploy with: pnpm run deploy:staging"
echo "3. Deploy to production with: pnpm run deploy"
echo ""
echo "For more details, see DEPLOYMENT.md"

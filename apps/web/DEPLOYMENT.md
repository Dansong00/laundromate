# 🚀 Vercel Deployment Guide for LaundroMate Frontend

This guide covers deploying your Next.js frontend to Vercel with proper environment configuration and deployment strategies.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm i -g vercel`
3. **GitHub Integration**: Connect your repository to Vercel

## 🛠️ Initial Setup

### 1. Install Vercel CLI

```bash
npm i -g vercel
# or
pnpm add -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Link Your Project

```bash
cd apps/web
vercel link
```

## 🌍 Environment Configuration

### Environment Variables by Stage

#### Development (Local)

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENVIRONMENT=development
```

#### Staging

```bash
# Set in Vercel Dashboard or via CLI
NEXT_PUBLIC_API_URL=https://your-staging-api.railway.app
NEXT_PUBLIC_APP_ENVIRONMENT=staging
```

#### Production

```bash
# Set in Vercel Dashboard or via CLI
NEXT_PUBLIC_API_URL=https://your-production-api.railway.app
NEXT_PUBLIC_APP_ENVIRONMENT=production
```

### Setting Environment Variables

#### Via Vercel CLI

```bash
# Set for production
vercel env add NEXT_PUBLIC_API_URL production

# Set for preview/staging
vercel env add NEXT_PUBLIC_API_URL preview
```

#### Via Vercel Dashboard

1. Go to your project in Vercel
2. Navigate to Settings → Environment Variables
3. Add variables for each environment

## 🚀 Deployment Commands

### Development/Preview Deployment

```bash
vercel
# or
pnpm run deploy:staging
```

### Production Deployment

```bash
vercel --prod
# or
pnpm run deploy
```

### Preview Deployment (for PRs)

```bash
vercel --preview
# or
pnpm run deploy:preview
```

## 🔄 CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/deploy-frontend.yml`:

```yaml
name: Deploy Frontend to Vercel

on:
  push:
    branches: [main]
    paths: ["apps/web/**"]
  pull_request:
    branches: [main]
    paths: ["apps/web/**"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: "npm"

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: |
          cd apps/web
          pnpm install

      - name: Build application
        run: |
          cd apps/web
          pnpm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

## 📊 Performance Optimization

### Vercel Analytics

Enable in your Vercel dashboard for performance monitoring.

### Image Optimization

- Use Next.js `Image` component
- Configure domains in `next.config.ts`
- Leverage Vercel's global CDN

### Bundle Analysis

```bash
# Analyze bundle size
pnpm add -D @next/bundle-analyzer
```

## 🔍 Troubleshooting

### Common Issues

#### Build Failures

- Check environment variables are set correctly
- Verify all dependencies are in `package.json`
- Check for TypeScript/ESLint errors

#### API Connection Issues

- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS configuration on backend
- Ensure backend is accessible from Vercel

#### Performance Issues

- Enable Vercel Analytics
- Check bundle size with bundle analyzer
- Optimize images and static assets

### Debug Commands

```bash
# Check Vercel configuration
vercel inspect

# View deployment logs
vercel logs

# Check environment variables
vercel env ls
```

## 🔐 Security Considerations

### Environment Variables

- Never commit `.env` files
- Use `NEXT_PUBLIC_` prefix only for client-side variables
- Keep sensitive data server-side only

### Headers Configuration

Security headers are configured in `vercel.json`:

- XSS Protection
- Content Type Options
- Frame Options
- CORS configuration

## 📈 Scaling Considerations

### Vercel Limits

- **Hobby Plan**: 100GB bandwidth/month
- **Pro Plan**: 1TB bandwidth/month
- **Enterprise**: Custom limits

### Performance Features

- Global CDN
- Edge Functions
- Automatic HTTPS
- Zero-downtime deployments

## 🔗 Next Steps

1. **Set up Vercel project** using the commands above
2. **Configure environment variables** for your API endpoints
3. **Test deployment** with staging environment
4. **Set up CI/CD** with GitHub Actions
5. **Monitor performance** with Vercel Analytics

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Environment Variables Best Practices](https://vercel.com/docs/projects/environment-variables)

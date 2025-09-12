# Quick CI/CD Setup Guide

## 🚀 Getting Started with CI/CD

This guide will help you set up the CI/CD pipeline for your LaundroMate project.

## Prerequisites

- GitHub repository with Actions enabled
- Railway account and CLI installed
- Node.js 18+ and Python 3.11+

## Step 1: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

```
RAILWAY_TOKEN=your_railway_production_token
RAILWAY_STAGING_TOKEN=your_railway_staging_token (optional)
RAILWAY_STAGING_PROJECT_ID=your_staging_project_id (optional)
```

### Getting Railway Tokens

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Generate token
railway auth:token
```

## Step 2: Test the Pipeline

1. **Push to develop branch** (triggers CI + staging deployment)
2. **Create a pull request** (triggers CI only)
3. **Merge to main** (triggers CI + production deployment)

## Step 3: Monitor Pipeline

- **GitHub Actions**: `https://github.com/[owner]/[repo]/actions`
- **Railway Dashboard**: `railway open`

## Step 4: Local Testing

```bash
# Run all CI checks locally
pnpm run ci

# Individual checks
pnpm run lint
pnpm run type-check
pnpm run test
pnpm run build
```

## Pipeline Flow

```
Push/PR → CI Pipeline → Quality Gates → Deploy (if main/develop)
   ↓
┌─────────────────────────────────────────────────────────┐
│ CI Pipeline Jobs:                                       │
│ • Test API (pytest + coverage)                          │
│ • Test Web (build + tests)                              │
│ • Lint API (black, isort, flake8)                       │
│ • Lint Web (ESLint)                                     │
│ • Type Check API (mypy)                                 │
│ • Type Check Web (TypeScript)                           │
│ • Security Scan (Safety + pnpm audit)                   │
└─────────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────────┐
│ Quality Gates:                                          │
│ ✅ All tests pass                                       │
│ ✅ All linting passes                                   │
│ ✅ All type checks pass                                 │
│ ✅ Security scans pass                                  │
│ ✅ All builds succeed                                    │
└─────────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────────┐
│ Deployment (only if all gates pass):                   │
│ • develop → staging environment                        │
│ • main → production environment                        │
└─────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Pipeline Failing?

1. **Check GitHub Actions logs**
2. **Run checks locally**: `pnpm run ci`
3. **Fix linting issues**: `pnpm run lint`
4. **Fix type errors**: `pnpm run type-check`

### Deployment Issues?

1. **Check Railway tokens**: `railway whoami`
2. **View Railway logs**: `railway logs`
3. **Check Railway status**: `railway status`

## Next Steps

1. **Add more tests** to improve coverage
2. **Set up staging environment** for testing
3. **Configure notifications** (Slack, email)
4. **Add E2E tests** (Playwright, Cypress)

## Need Help?

- Check the full documentation: `CI-CD-PIPELINE.md`
- Review GitHub Actions logs
- Contact the development team

---

**🎉 Your CI/CD pipeline is now ready!**
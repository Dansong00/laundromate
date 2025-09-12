# CI/CD Pipeline Documentation

## Overview

This document describes the comprehensive CI/CD pipeline implemented for the LaundroMate project. The pipeline ensures code quality, runs tests, performs static analysis, and deploys only when all checks pass.

## Pipeline Architecture

### Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Runs on every push and pull request to `main` and `develop` branches
   - Performs comprehensive testing, linting, type checking, and security scanning
   - Must pass before deployment can occur

2. **Deploy Pipeline** (`.github/workflows/deploy.yml`)
   - Runs only after CI pipeline passes successfully
   - Deploys to production (main branch) and staging (develop branch)
   - Uses Railway for deployment

## CI Pipeline Jobs

### 1. Test API (`test-api`)
- **Purpose**: Run comprehensive tests for the FastAPI backend
- **Services**: PostgreSQL 15, Redis 7
- **Tools**: pytest with coverage reporting
- **Coverage**: Uploads coverage reports to Codecov
- **Environment**: Test database and Redis instances

### 2. Test Web App (`test-web`)
- **Purpose**: Run tests and build the Next.js frontend
- **Tools**: pnpm, Next.js build system
- **Fallback**: Gracefully handles missing test scripts

### 3. Lint API (`lint-api`)
- **Purpose**: Code quality checks for Python backend
- **Tools**: 
  - Black (code formatting)
  - isort (import sorting)
  - flake8 (linting)
- **Scope**: `app/` and `tests/` directories

### 4. Lint Web App (`lint-web`)
- **Purpose**: Code quality checks for TypeScript/React frontend
- **Tools**: ESLint with Next.js configuration
- **Scope**: All TypeScript/JavaScript files

### 5. Type Check API (`type-check-api`)
- **Purpose**: Static type checking for Python code
- **Tools**: mypy with strict configuration
- **Scope**: `app/` directory

### 6. Type Check Web App (`type-check-web`)
- **Purpose**: Static type checking for TypeScript code
- **Tools**: TypeScript compiler (`tsc --noEmit`)
- **Scope**: All TypeScript files

### 7. Security Scan (`security-scan`)
- **Purpose**: Security vulnerability scanning
- **Tools**: 
  - Safety (Python dependencies)
  - pnpm audit (Node.js dependencies)
- **Level**: Moderate severity and above

## Deployment Pipeline

### Production Deployment (`deploy`)
- **Trigger**: Push to `main` branch OR successful CI pipeline completion
- **Condition**: Only runs if CI pipeline passes
- **Environment**: Production Railway deployment
- **Steps**:
  1. Build all applications
  2. Deploy to Railway using CLI
  3. Verify deployment status

### Staging Deployment (`deploy-staging`)
- **Trigger**: Push to `develop` branch with successful CI
- **Environment**: Staging Railway deployment
- **Purpose**: Pre-production testing environment

## Required Secrets

Configure these secrets in your GitHub repository settings:

### Railway Tokens
- `RAILWAY_TOKEN`: Production deployment token
- `RAILWAY_STAGING_TOKEN`: Staging deployment token (optional)
- `RAILWAY_STAGING_PROJECT_ID`: Staging project ID (optional)

### How to Get Railway Tokens
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Generate token: `railway auth:token`
4. Add to GitHub Secrets

## Local Development

### Running CI Checks Locally

```bash
# Install dependencies
pnpm install

# Run all CI checks
pnpm run ci

# Individual checks
pnpm run lint          # Lint all packages
pnpm run type-check    # Type check all packages
pnpm run test          # Run all tests
pnpm run build         # Build all packages
```

### Backend (API) Checks
```bash
cd apps/api

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=app --cov-report=term-missing

# Run linting
black --check app tests
isort --check-only app tests
flake8 app tests

# Run type checking
mypy app

# Run security scan
safety check
```

### Frontend (Web) Checks
```bash
cd apps/web

# Install dependencies
pnpm install

# Run linting
pnpm run lint

# Run type checking
pnpm run type-check

# Build application
pnpm run build

# Run security audit
pnpm audit --audit-level moderate
```

## Pipeline Triggers

### Automatic Triggers
- **Push to `main`**: Runs CI → Deploys to production
- **Push to `develop`**: Runs CI → Deploys to staging
- **Pull Request**: Runs CI only (no deployment)

### Manual Triggers
- **Workflow Dispatch**: Can manually trigger any workflow
- **Repository Dispatch**: External triggers via API

## Quality Gates

The pipeline implements strict quality gates:

1. **All tests must pass** (API and Web)
2. **All linting checks must pass** (Black, isort, flake8, ESLint)
3. **All type checks must pass** (mypy, TypeScript)
4. **Security scans must pass** (Safety, pnpm audit)
5. **Builds must succeed** (All packages)

**Deployment only occurs if ALL quality gates pass.**

## Monitoring and Notifications

### GitHub Actions Dashboard
- View pipeline status: `https://github.com/[owner]/[repo]/actions`
- Check individual job logs
- Monitor deployment status

### Railway Dashboard
- View deployment logs: `railway logs`
- Monitor service health: `railway status`
- Open dashboard: `railway open`

## Troubleshooting

### Common Issues

1. **Tests Failing**
   - Check test database connectivity
   - Verify test data setup
   - Review test coverage requirements

2. **Linting Failures**
   - Run `black .` to auto-format Python code
   - Run `isort .` to auto-sort imports
   - Fix ESLint errors in TypeScript files

3. **Type Check Failures**
   - Fix mypy errors in Python code
   - Fix TypeScript errors in frontend code
   - Update type definitions as needed

4. **Deployment Failures**
   - Verify Railway tokens are valid
   - Check Railway service limits
   - Review deployment logs

### Debug Commands

```bash
# Check Railway connection
railway whoami

# View Railway logs
railway logs --follow

# Check Railway status
railway status

# Test local builds
pnpm run build
cd apps/api && python -m pip install -e ".[dev]"
```

## Best Practices

### Code Quality
- Write tests for new features
- Maintain high test coverage
- Follow linting rules consistently
- Use proper TypeScript types

### Deployment
- Test changes in staging first
- Use feature branches for development
- Review all changes via pull requests
- Monitor deployment health

### Security
- Keep dependencies updated
- Review security audit results
- Use environment variables for secrets
- Follow security best practices

## Future Enhancements

### Planned Improvements
1. **E2E Testing**: Add Playwright or Cypress tests
2. **Performance Testing**: Add Lighthouse CI
3. **Dependency Updates**: Automated dependency updates
4. **Slack Notifications**: Deployment notifications
5. **Rollback Strategy**: Automated rollback on failures
6. **Multi-environment**: Additional staging environments

### Monitoring
1. **Application Metrics**: Add monitoring and alerting
2. **Error Tracking**: Integrate Sentry or similar
3. **Performance Monitoring**: Add APM tools
4. **Uptime Monitoring**: External uptime checks

## Support

For questions or issues with the CI/CD pipeline:

1. Check the GitHub Actions logs
2. Review this documentation
3. Check Railway deployment status
4. Contact the development team

---

*Last updated: January 2025*
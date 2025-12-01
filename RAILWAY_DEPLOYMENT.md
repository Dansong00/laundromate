# 🚂 Railway Full-Stack Deployment Guide

This guide covers deploying your entire LaundroMate application (frontend, backend, database, and Redis) to Railway using a monorepo approach.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install globally with `npm install -g @railway/cli`
3. **GitHub Repository**: Your code should be in a Git repository
4. **Docker**: Ensure your Dockerfiles are properly configured

## 🏗️ Project Structure

```
LaundroMate/
├── railway.json              # Root Railway configuration
├── railway-services.json     # Service definitions
├── deploy-railway.sh        # Deployment script
├── apps/
│   ├── api/
│   │   ├── railway.json     # API service config
│   │   └── Dockerfile       # API container
│   └── web/
│       ├── railway.json     # Web service config
│       └── Dockerfile       # Web container
└── .github/workflows/
    └── deploy-railway.yml   # CI/CD workflow
```

## 🚀 Initial Setup

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login to Railway
```bash
railway login
```

### 3. Create New Project
```bash
railway init
```

### 4. Link Your Project
```bash
railway link
```

## 🔧 Service Configuration

### API Service (FastAPI)
- **Source**: `apps/api`
- **Build Command**: Auto-detected from Dockerfile
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Port**: Railway auto-assigns

### Web Service (Next.js)
- **Source**: `apps/web`
- **Build Command**: Auto-detected from Dockerfile
- **Start Command**: `npm start`
- **Port**: Railway auto-assigns

### Database Service (PostgreSQL)
- **Type**: Managed PostgreSQL
- **Variables**: Auto-configured by Railway

### Redis Service
- **Type**: Managed Redis
- **Variables**: Auto-configured by Railway

## 🌍 Environment Variables

### API Service Variables
```bash
DATABASE_URL={{.Postgres.DATABASE_URL}}
REDIS_URL={{.Redis.REDIS_URL}}
SECRET_KEY={{.Secret.SECRET_KEY}}
ENVIRONMENT=production
```

### Web Service Variables
```bash
NEXT_PUBLIC_API_URL={{.laundromate-api.PUBLIC_URL}}
NEXT_PUBLIC_APP_ENVIRONMENT=production
```

### Setting Environment Variables

#### Via Railway CLI
```bash
# Set for API service
railway env set DATABASE_URL "your-database-url" --service laundromate-api

# Set for web service
railway env set NEXT_PUBLIC_API_URL "your-api-url" --service laundromate-web
```

#### Via Railway Dashboard
1. Go to your project in Railway
2. Select the service
3. Navigate to Variables tab
4. Add/update variables

## 🚀 Deployment

### Manual Deployment
```bash
# Deploy all services
railway up

# Deploy specific service
railway up --service laundromate-api

# Deploy with logs
railway up --logs
```

### Using Deployment Script
```bash
./deploy-railway.sh
```

### Automated Deployment (GitHub Actions)
The workflow automatically deploys on:
- Push to `main` branch
- Pull requests to `main` branch

## 📊 Monitoring & Management

### View Logs
```bash
# All services
railway logs

# Specific service
railway logs --service laundromate-api

# Follow logs
railway logs --follow
```

### Service Status
```bash
# List all services
railway service list

# Service details
railway service show laundromate-api
```

### Open Dashboard
```bash
railway open
```

## 🔍 Troubleshooting

### Common Issues

#### Build Failures
- Check Dockerfile syntax
- Verify dependencies in requirements.txt/package.json
- Check build logs in Railway dashboard

#### Service Communication Issues
- Verify environment variables are set correctly
- Check service names match in railway-services.json
- Ensure CORS is configured on the API

#### Database Connection Issues
- Verify DATABASE_URL format
- Check PostgreSQL service is running
- Verify database credentials

### Debug Commands
```bash
# Check Railway configuration
railway status

# View service logs
railway logs --service laundromate-api

# Check environment variables
railway variables --service laundromate-api

# Restart service
railway service restart laundromate-api
```

## 🔐 Security Considerations

### Environment Variables
- Never commit `.env` files
- Use Railway's built-in secret management
- Rotate secrets regularly

### Service Communication
- Services communicate via internal Railway network
- External access controlled via Railway domains
- HTTPS enabled by default

## 📈 Scaling

### Railway Plans
- **Hobby**: $5/month + usage
- **Pro**: $20/month + usage
- **Enterprise**: Custom pricing

### Auto-scaling
- Railway automatically scales based on traffic
- Configure resource limits per service
- Monitor usage in dashboard

## 🔄 CI/CD Integration

### GitHub Actions Setup
1. Add `RAILWAY_TOKEN` to repository secrets
2. Push to trigger automatic deployment
3. Monitor deployment status in Actions tab

### Manual Deployment
```bash
# Deploy from specific branch
railway up --branch feature-branch

# Deploy with custom environment
railway up --environment staging
```

## 🎯 Next Steps

1. **Test deployment** with staging environment
2. **Configure custom domains** for production
3. **Set up monitoring** and alerts
4. **Configure backups** for database
5. **Set up SSL certificates** (automatic with Railway)

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/reference/cli)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 🆘 Support

- **Railway Support**: [support.railway.app](https://support.railway.app)
- **Community Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Use your repository's issue tracker

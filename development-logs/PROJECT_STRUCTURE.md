# LaundroMate Project Structure

## 📁 Monorepo Overview

```
LaundroMate/
├── apps/                          # Applications
│   ├── web/                       # Next.js Frontend
│   │   ├── src/
│   │   │   ├── app/              # App Router pages
│   │   │   ├── components/       # React components
│   │   │   ├── lib/             # Utilities and helpers
│   │   │   └── types/           # TypeScript types
│   │   ├── public/              # Static assets
│   │   └── package.json
│   └── api/                      # FastAPI Backend
│       ├── app/
│       │   ├── auth/            # Authentication module
│       │   ├── customers/       # Customer management
│       │   ├── orders/          # Order management
│       │   ├── notifications/   # Notification system
│       │   └── core/            # Core functionality
│       │       ├── database/    # Database models
│       │       ├── models/      # SQLAlchemy models
│       │       ├── schemas/     # Pydantic schemas
│       │       └── config/      # Configuration
│       ├── alembic/             # Database migrations
│       └── requirements.txt
├── packages/                     # Shared packages
│   ├── ui/                      # Shared UI components
│   │   ├── src/
│   │   │   ├── components/      # React components
│   │   │   └── utils/          # Utility functions
│   │   └── package.json
│   ├── types/                   # Shared TypeScript types
│   │   ├── src/
│   │   └── package.json
│   └── utils/                   # Shared utilities
│       ├── src/
│       └── package.json
├── docker-compose.yml           # Development environment
├── package.json                 # Root package.json
├── pnpm-workspace.yaml         # pnpm workspace config
└── tsconfig.json               # Root TypeScript config
```

## 🏗 Architecture

### Frontend (Next.js 14 + App Router)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **State Management**: React hooks + Context API
- **UI Components**: Custom component library (@laundromate/ui)

### Backend (FastAPI)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Async Tasks**: Celery with Redis
- **Documentation**: Auto-generated OpenAPI/Swagger

### Shared Packages
- **@laundromate/types**: Shared TypeScript interfaces
- **@laundromate/ui**: Reusable React components
- **@laundromate/utils**: Utility functions

## 🚀 Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- pnpm
- Docker & Docker Compose

### Quick Start
1. **Clone and install dependencies**:
   ```bash
   git clone <repository-url>
   cd LaundroMate
   pnpm install
   ```

2. **Start development environment**:
   ```bash
   # Start all services (database, redis, api, web)
   docker-compose up -d

   # Or start individual services
   pnpm dev:web    # Frontend only
   pnpm dev:api    # Backend only
   ```

3. **Access applications**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📦 Package Management

### Root Commands
```bash
pnpm dev          # Start frontend development server
pnpm dev:api      # Start backend development server
pnpm build        # Build all packages
pnpm lint         # Lint all packages
pnpm type-check   # Type check all packages
```

### Individual Package Commands
```bash
# Frontend
cd apps/web
pnpm dev          # Start development server
pnpm build        # Build for production

# Backend
cd apps/api
uvicorn app.main:app --reload  # Start development server

# Shared packages
cd packages/ui
pnpm build        # Build component library
pnpm dev          # Watch mode for development
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in the respective app directories:

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env)**:
```env
DATABASE_URL=postgresql://laundromate:laundromate@localhost:5432/laundromate
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379
```

## 🗄 Database

### Initial Setup
```bash
# Start PostgreSQL
docker-compose up postgres -d

# Run migrations (after setting up Alembic)
cd apps/api
alembic upgrade head
```

### Migration Commands
```bash
cd apps/api
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1
```

## 🧪 Testing

### Frontend Testing
```bash
cd apps/web
pnpm test         # Run tests
pnpm test:watch   # Watch mode
```

### Backend Testing
```bash
cd apps/api
pytest            # Run tests
pytest -v         # Verbose output
```

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **TypeScript Types**: See `packages/types/src/index.ts`
- **Component Library**: See `packages/ui/src/components/`

## 🔄 Development Workflow

1. **Feature Development**:
   - Create feature branch from `main`
   - Develop in respective app directory
   - Use shared packages for common functionality
   - Test locally with Docker Compose

2. **Package Updates**:
   - Update shared packages first
   - Build and link packages
   - Update consuming applications

3. **Deployment**:
   - Build all packages: `pnpm build`
   - Deploy using Docker images
   - Run database migrations

## 🎯 Next Steps

1. **Authentication System**: Implement JWT-based auth
2. **Database Models**: Create SQLAlchemy models
3. **API Endpoints**: Build RESTful API routes
4. **UI Components**: Develop component library
5. **Integration**: Connect frontend to backend
6. **Testing**: Add comprehensive test coverage

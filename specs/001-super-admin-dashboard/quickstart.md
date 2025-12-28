# Quickstart: Super-User Admin Dashboard

**Feature**: Super-User Admin Dashboard (Control Room)
**Date**: 2025-12-27

## Overview

This guide provides a quick start for implementing the Super-User Admin Dashboard feature. Follow these steps to set up the development environment and begin implementation.

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ and pnpm installed
- PostgreSQL database running (via Docker Compose or local installation)
- Redis running (for Celery tasks, if needed)
- Git repository cloned and dependencies installed

## Setup Steps

### 1. Database Migration

Create and apply Alembic migration for new tables:

```bash
cd apps/api
alembic revision --autogenerate -m "Add super admin dashboard models"
alembic upgrade head
```

This creates:
- `organizations` table
- `stores` table
- `iot_controllers` table
- `agent_configurations` table
- `ai_agents` table (seeded with initial agents)

### 2. Seed Initial Data

Seed the `ai_agents` table with initial agent definitions:

```python
# Run in Python shell or create a migration script
from app.core.database.session import SessionLocal
from app.core.models.ai_agent import AIAgent

db = SessionLocal()
agents = [
    AIAgent(id="maintenance_prophet", name="Maintenance Prophet", category="maintenance", is_available=True),
    AIAgent(id="pricing_strategist", name="Pricing Strategist", category="pricing", is_available=True),
]
for agent in agents:
    db.merge(agent)  # Use merge to avoid duplicates
db.commit()
```

### 3. Backend API Setup

Create new router modules following existing patterns:

```bash
# Create router directories
mkdir -p apps/api/app/organizations
mkdir -p apps/api/app/stores
mkdir -p apps/api/app/iot
mkdir -p apps/api/app/agents
mkdir -p apps/api/app/health

# Create __init__.py files
touch apps/api/app/organizations/__init__.py
touch apps/api/app/stores/__init__.py
touch apps/api/app/iot/__init__.py
touch apps/api/app/agents/__init__.py
touch apps/api/app/health/__init__.py
```

### 4. Frontend Setup

Create new Next.js routes under `/super-admin`:

```bash
# Create route directories
mkdir -p apps/web/src/app/super-admin/organizations
mkdir -p apps/web/src/app/super-admin/stores
mkdir -p apps/web/src/app/super-admin/health
```

### 5. Shared Types

Add TypeScript interfaces to `packages/types/src/index.ts`:

```typescript
// Organization types
export interface Organization {
  id: string;
  name: string;
  billing_address: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  contact_email?: string;
  contact_phone?: string;
  status: 'active' | 'inactive' | 'suspended';
  created_at: string;
  updated_at: string;
}

// Store types
export interface Store {
  id: string;
  organization_id: string;
  name: string;
  street_address: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}

// IoT Controller types
export interface IoTController {
  id: string;
  store_id: string;
  mac_address: string;
  serial_number?: string;
  machine_label: string;
  device_type: 'washer' | 'dryer' | 'other';
  connectivity_status: 'online' | 'offline' | 'unknown';
  last_heartbeat?: string;
  provisioned_at: string;
  created_at: string;
  updated_at: string;
}

// Agent Configuration types
export interface AgentConfiguration {
  id: string;
  store_id: string;
  enabled_agents: string[];
  last_updated_at: string;
  last_updated_by: string;
  created_at: string;
  updated_at: string;
}

// System Health types
export interface SystemHealthStatus {
  store_id: string;
  store_name: string;
  organization_name: string;
  connectivity_status: 'online' | 'offline' | 'partial' | 'unknown';
  online_controllers: number;
  offline_controllers: number;
  total_controllers: number;
  last_heartbeat?: string;
  alert_count: number;
  critical_alerts: number;
}
```

## Development Workflow

### Backend Development

1. **Create Models**: Start with `app/core/models/organization.py`, following existing model patterns
2. **Create Schemas**: Add Pydantic schemas in `app/core/schemas/organization.py`
3. **Create Repository**: Implement repository in `app/core/repositories/organization_repository.py`
4. **Create Router**: Add FastAPI router in `app/organizations/router.py`
5. **Write Tests**: Add unit and integration tests in `tests/unit/` and `tests/integration/`

### Frontend Development

1. **Create API Client**: Add functions to `apps/web/src/lib/api/super-admin.ts`
2. **Create Components**: Build components in `apps/web/src/components/admin/`
3. **Create Pages**: Add Next.js pages in `apps/web/src/app/super-admin/`
4. **Use Server Components**: Prefer Server Components; use Client Components only for interactivity

## Testing

### Backend Tests

```bash
cd apps/api
pytest tests/unit/domain/test_organizations.py -v
pytest tests/integration/test_organizations_routes.py -v
```

### Frontend Tests (if using Jest)

```bash
cd apps/web
pnpm test
```

## API Testing

Use the OpenAPI schema at `specs/001-super-admin-dashboard/contracts/openapi.yaml`:

1. Import into Postman or Insomnia
2. Set up authentication with JWT token
3. Test endpoints in order:
   - Create organization
   - Create store
   - Provision IoT controller
   - Configure agents
   - Check health status

## Common Tasks

### Create a New Organization

```bash
curl -X POST http://localhost:8000/super-admin/organizations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunny Laundromat LLC",
    "billing_address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94102",
    "country": "US",
    "contact_email": "contact@sunny.com"
  }'
```

### Provision an IoT Controller

```bash
curl -X POST http://localhost:8000/super-admin/stores/{store_id}/iot \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "machine_label": "Washer #1",
    "device_type": "washer"
  }'
```

### Enable an Agent

```bash
curl -X PUT http://localhost:8000/super-admin/stores/{store_id}/agents \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled_agents": ["maintenance_prophet", "pricing_strategist"]
  }'
```

## Next Steps

1. Review the [data model](./data-model.md) for entity relationships
2. Review the [API contracts](./contracts/openapi.yaml) for endpoint specifications
3. Follow the [implementation plan](./plan.md) for detailed architecture
4. Check the [specification](./spec.md) for functional requirements

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker compose ps postgres

# Test connection
docker compose exec postgres psql -U laundromate -d laundromate -c "SELECT 1;"
```

### Migration Issues

```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Rollback if needed
alembic downgrade -1
```

### Type Errors

```bash
# Backend type checking
cd apps/api
mypy app/

# Frontend type checking
cd apps/web
pnpm type-check
```

## Resources

- [Constitution](../../.specify/memory/constitution.md) - Project principles and standards
- [Specification](./spec.md) - Feature requirements
- [Data Model](./data-model.md) - Entity definitions
- [API Contracts](./contracts/openapi.yaml) - OpenAPI schema

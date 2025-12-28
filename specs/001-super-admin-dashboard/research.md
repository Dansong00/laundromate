# Research: Super-User Admin Dashboard

**Feature**: Super-User Admin Dashboard (Control Room)
**Date**: 2025-12-27
**Status**: Complete

## Overview

No significant research was required as this feature extends existing patterns and infrastructure. All technical decisions align with the established codebase architecture and constitution requirements.

## Technical Decisions

### Database Architecture
- **Decision**: Use existing PostgreSQL database with new tables via Alembic migrations
- **Rationale**: Consistent with existing data persistence strategy; leverages existing database connection pooling and transaction management
- **Alternatives Considered**: Separate database (rejected - adds complexity without benefit)

### Role-Based Access Control
- **Decision**: Extend existing User model with role-based permissions (Super-Admin, Support Agent, Provisioning Specialist)
- **Rationale**: User model already has `is_super_admin` and `is_admin` flags; will add role enum or additional flags for new roles
- **Alternatives Considered**: Separate role table (rejected - simpler to extend existing model for internal staff roles)

### API Architecture
- **Decision**: Follow existing FastAPI router pattern with dependency injection
- **Rationale**: Consistent with existing `/auth`, `/customers`, `/orders` routers; maintains separation of concerns
- **Alternatives Considered**: GraphQL (rejected - REST API already established)

### Frontend Architecture
- **Decision**: Extend existing Next.js App Router structure under `/super-admin` route
- **Rationale**: Consistent with existing `/admin` and `/portal` routes; leverages Server Components by default
- **Alternatives Considered**: Separate admin application (rejected - adds deployment complexity)

### IoT Controller Identification
- **Decision**: Use MAC address as primary identifier, serial number as optional secondary identifier
- **Rationale**: MAC addresses are unique per device and standard for network device identification
- **Alternatives Considered**: UUID generation (rejected - MAC address is hardware-bound and more reliable)

### Agent Configuration Storage
- **Decision**: Store agent enable/disable state per store in database (many-to-many relationship)
- **Rationale**: Allows flexible subscription management; enables audit trail of configuration changes
- **Alternatives Considered**: Feature flags service (rejected - overkill for current scale; database is sufficient)

### Real-Time Health Monitoring
- **Decision**: Poll-based health status updates (30-second refresh) rather than WebSocket
- **Rationale**: Simpler implementation; sufficient for internal dashboard use; reduces infrastructure complexity
- **Alternatives Considered**: WebSocket/SSE (rejected - adds complexity; polling is acceptable for internal tool)

### Shadow View Implementation
- **Decision**: Render operator dashboard with read-only mode and audit logging
- **Rationale**: Reuses existing operator dashboard components; read-only mode prevents accidental data modification
- **Alternatives Considered**: Separate shadow view components (rejected - code duplication; reuse is better)

## Patterns and Best Practices

### Repository Pattern
- Following existing repository pattern from `app/core/repositories/base.py`
- All database access through repository interfaces
- Enables testability and future data source changes

### Pydantic Validation
- Using Pydantic 2.x for request/response validation
- Consistent with existing schema patterns in `app/core/schemas/`
- Type-safe API contracts

### Dependency Injection
- Using FastAPI `Depends()` for database sessions and authentication
- Consistent with existing route handlers
- Enables easy testing with dependency overrides

### Type Safety
- TypeScript strict mode for frontend
- Python type hints with mypy for backend
- Shared types in `@laundromate/types` package

## No Blocking Issues

All technical decisions are straightforward extensions of existing patterns. No research gaps or unknowns that would block implementation.

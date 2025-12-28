# Implementation Plan: Super-User Admin Dashboard (Control Room)

**Branch**: `001-super-admin-dashboard` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-super-admin-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Super-User Admin Dashboard (Control Room) enables LaundroMate internal staff to provision new customer organizations and stores, configure IoT hardware mappings, manage AI agent subscriptions, and monitor system health. This is a web application built on the existing Next.js frontend and FastAPI backend, extending the current super-admin portal with comprehensive administrative capabilities. The feature requires new database models for Organizations, Stores, IoT Controllers, and Agent Configurations, along with role-based access control for three internal user types: Super-Admin, Support Agent, and Provisioning Specialist.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5+
**Primary Dependencies**: FastAPI 0.104.1, Next.js 14.2.0, React 18.2.0, SQLAlchemy 2.0.23, Pydantic 2.5.0
**Storage**: PostgreSQL (existing database, new tables via Alembic migrations)
**Testing**: pytest 7.0+ with pytest-asyncio, pytest-cov for backend; Jest/React Testing Library for frontend (if needed)
**Target Platform**: Web application (Next.js App Router), Linux server (FastAPI)
**Project Type**: Web application (monorepo with frontend and backend)
**Performance Goals**: API endpoints respond within 200ms p95 latency; dashboard loads within 2 seconds; real-time health status updates within 30 seconds
**Constraints**: Must maintain existing authentication/authorization patterns; must integrate with existing User model; must support role-based access control (Super-Admin, Support Agent, Provisioning Specialist); must comply with constitution performance requirements (<200ms API p95)
**Scale/Scope**: Support 100+ organizations, 500+ stores, 1000+ IoT controllers; handle 50+ concurrent internal staff users; process 10,000+ health status updates per day

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Type Safety First ✓
- **Compliance**: All new TypeScript code will use strict mode; all Python functions will have type hints; Pydantic models for API validation; TypeScript interfaces in `@laundromate/types` for shared contracts.
- **Status**: PASS - Existing codebase already follows these patterns.

### Testing Discipline (NON-NEGOTIABLE) ✓
- **Compliance**: Unit tests for all business logic (organizations, stores, IoT mapping, agent configuration); integration tests for all API endpoints; target 80%+ coverage for new code; critical paths (onboarding, IoT mapping) require 95%+ coverage.
- **Status**: PASS - Testing infrastructure exists; plan includes comprehensive test coverage.

### User Experience Consistency ✓
- **Compliance**: Use `@laundromate/ui` design system components; follow established patterns for forms, tables, and dashboards; maintain accessibility (WCAG 2.1 AA); responsive design for desktop (primary) and tablet.
- **Status**: PASS - Design system exists; will extend existing component library.

### Performance Requirements ✓
- **Compliance**: API endpoints must respond within 200ms p95; database queries optimized with indexes; pagination for list endpoints; code splitting for dashboard routes; Server Components by default.
- **Status**: PASS - Performance targets align with constitution; will use existing optimization patterns.

### Next.js & TypeScript Architecture Patterns ✓
- **Compliance**: Use App Router for new routes; Server Components by default; Client Components only for interactivity; API routes in `app/api/`; shared types in `@laundromate/types`.
- **Status**: PASS - Existing codebase follows these patterns; will extend consistently.

### Python & FastAPI Architecture Patterns ✓
- **Compliance**: Use dependency injection via `Depends()`; separate business logic from route handlers; use Repository pattern for database access; Pydantic models for validation; async/await for all operations.
- **Status**: PASS - Existing codebase follows these patterns; will extend consistently.

### Code Quality & Formatting Standards ✓
- **Compliance**: All code must pass ESLint (frontend) and Flake8 (backend); Black formatting for Python; Prettier/ESLint for TypeScript; small focused functions; self-documenting code.
- **Status**: PASS - Existing tooling in place; will follow established patterns.

### Security & Data Protection ✓
- **Compliance**: JWT authentication (existing); role-based authorization; input validation via Pydantic; SQL injection protection via ORM; environment variables for secrets; audit logging for Shadow View.
- **Status**: PASS - Security patterns established; will extend with new role checks.

**Overall Status**: ✅ ALL GATES PASS - No violations detected. Implementation can proceed.

## Project Structure

### Documentation (this feature)

```text
specs/001-super-admin-dashboard/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
apps/web/
├── src/
│   ├── app/
│   │   ├── super-admin/
│   │   │   ├── page.tsx                    # Existing super-admin landing (extend)
│   │   │   ├── organizations/
│   │   │   │   ├── page.tsx                # Organization list
│   │   │   │   ├── new/
│   │   │   │   │   └── page.tsx            # Onboarding wizard
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx            # Organization detail
│   │   │   │       └── stores/
│   │   │   │           ├── page.tsx        # Store list
│   │   │   │           └── new/
│   │   │   │               └── page.tsx    # Add store
│   │   │   ├── stores/
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx            # Store detail
│   │   │   │       ├── iot/
│   │   │   │       │   └── page.tsx        # IoT mapping interface
│   │   │   │       └── agents/
│   │   │   │           └── page.tsx        # Agent configuration
│   │   │   ├── health/
│   │   │   │   └── page.tsx                # System health dashboard
│   │   │   └── shadow-view/
│   │   │       └── [storeId]/
│   │   │           └── page.tsx            # Shadow view (P3)
│   │   └── api/
│   │       └── super-admin/
│   │           ├── organizations/
│   │           │   ├── route.ts            # List/create organizations
│   │           │   └── [id]/
│   │           │       └── route.ts       # Get/update organization
│   │           ├── stores/
│   │           │   ├── route.ts            # List/create stores
│   │           │   └── [id]/
│   │           │       ├── route.ts        # Get/update store
│   │           │       ├── iot/
│   │           │       │   └── route.ts   # IoT controller management
│   │           │       └── agents/
│   │           │           └── route.ts  # Agent configuration
│   │           ├── health/
│   │           │   └── route.ts           # Health status endpoint
│   │           └── users/
│   │               └── [id]/
│   │                   └── reset-password/
│   │                       └── route.ts   # Password reset
│   ├── components/
│   │   ├── admin/
│   │   │   ├── OrganizationWizard.tsx      # Onboarding wizard
│   │   │   ├── StoreList.tsx                # Store listing
│   │   │   ├── IoTMappingTable.tsx         # IoT controller mapping
│   │   │   ├── AgentConfiguration.tsx      # Agent toggles
│   │   │   ├── HealthDashboard.tsx         # System health view
│   │   │   └── ShadowView.tsx              # Shadow view component (P3)
│   │   └── ui/                              # Existing design system
│   └── lib/
│       └── api/
│           └── super-admin.ts              # API client functions

apps/api/
├── app/
│   ├── organizations/
│   │   ├── __init__.py
│   │   └── router.py                       # Organization endpoints
│   ├── stores/
│   │   ├── __init__.py
│   │   └── router.py                       # Store endpoints
│   ├── iot/
│   │   ├── __init__.py
│   │   └── router.py                       # IoT controller endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   └── router.py                       # Agent configuration endpoints
│   ├── health/
│   │   ├── __init__.py
│   │   └── router.py                       # Health monitoring endpoints
│   ├── core/
│   │   ├── models/
│   │   │   ├── organization.py             # Organization model
│   │   │   ├── store.py                    # Store model
│   │   │   ├── iot_controller.py            # IoT Controller model
│   │   │   ├── agent_configuration.py      # Agent Configuration model
│   │   │   └── ai_agent.py                 # AI Agent model
│   │   ├── schemas/
│   │   │   ├── organization.py             # Organization schemas
│   │   │   ├── store.py                    # Store schemas
│   │   │   ├── iot_controller.py            # IoT Controller schemas
│   │   │   ├── agent_configuration.py      # Agent Configuration schemas
│   │   │   └── ai_agent.py                 # AI Agent schemas
│   │   └── repositories/
│   │       ├── organization_repository.py  # Organization repository
│   │       ├── store_repository.py         # Store repository
│   │       ├── iot_controller_repository.py # IoT Controller repository
│   │       └── agent_configuration_repository.py # Agent Configuration repository
│   └── auth/
│       └── decorators.py                   # Extend with new role checks

tests/
├── unit/
│   ├── domain/
│   │   ├── test_organizations.py           # Organization business logic
│   │   ├── test_stores.py                  # Store business logic
│   │   ├── test_iot_mapping.py             # IoT mapping logic
│   │   └── test_agent_configuration.py     # Agent configuration logic
│   └── database/
│       ├── test_models_organization.py    # Organization model tests
│       ├── test_models_store.py            # Store model tests
│       ├── test_models_iot_controller.py   # IoT Controller model tests
│       └── test_models_agent_configuration.py # Agent Configuration model tests
└── integration/
    ├── test_organizations_routes.py        # Organization API tests
    ├── test_stores_routes.py               # Store API tests
    ├── test_iot_routes.py                  # IoT API tests
    ├── test_agents_routes.py               # Agent API tests
    └── test_health_routes.py               # Health API tests
```

**Structure Decision**: This is a web application (monorepo) with frontend (Next.js) and backend (FastAPI). The feature extends the existing super-admin portal with new routes, components, and API endpoints. New database models are added to the existing `app/core/models/` structure, following the established repository pattern. Frontend components extend the existing `@laundromate/ui` design system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All architecture decisions align with existing patterns and constitution requirements.

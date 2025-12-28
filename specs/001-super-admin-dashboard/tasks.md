# Tasks: Super-User Admin Dashboard (Control Room)

**Input**: Design documents from `/specs/001-super-admin-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as per constitution requirements (80%+ coverage for new code, 95%+ for critical paths like onboarding and IoT mapping).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `apps/web/src/`, `apps/api/app/`
- **Backend**: `apps/api/app/`
- **Tests**: `apps/api/tests/`
- **Shared types**: `packages/types/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory structure for super-admin feature in apps/web/src/app/super-admin/
- [ ] T002 [P] Create directory structure for backend routers in apps/api/app/organizations/, apps/api/app/stores/, apps/api/app/iot/, apps/api/app/agents/, apps/api/app/health/
- [ ] T003 [P] Install @tanstack/react-query dependency in apps/web/package.json
- [ ] T004 [P] Create base API client utility in apps/web/src/lib/api/client.ts with apiFetch helper function

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create Alembic migration for new database tables (organizations, stores, iot_controllers, agent_configurations, ai_agents, invitations, user_stores) and add is_support_agent and is_provisioning_specialist columns to users table in apps/api/alembic/versions/
- [ ] T006 [P] Create Organization SQLAlchemy model in apps/api/app/core/models/organization.py
- [ ] T007 [P] Create Store SQLAlchemy model in apps/api/app/core/models/store.py
- [ ] T008 [P] Create IoT Controller SQLAlchemy model in apps/api/app/core/models/iot_controller.py
- [ ] T009 [P] Create Agent Configuration SQLAlchemy model in apps/api/app/core/models/agent_configuration.py
- [ ] T010 [P] Create AI Agent SQLAlchemy model in apps/api/app/core/models/ai_agent.py
- [ ] T010a [P] Create Invitation SQLAlchemy model in apps/api/app/core/models/invitation.py with fields: token, email, store_id, invited_by, status (enum), expires_at, accepted_at, created_at (see spec.md and data-model.md for details)
- [ ] T010b [P] Create User-Store association SQLAlchemy model (user_stores table) in apps/api/app/core/models/user_store.py for many-to-many relationship with role field (enum: owner, operator)
- [ ] T011 Update apps/api/app/core/models/__init__.py to export all new models
- [ ] T012 Run Alembic migration to create tables: alembic upgrade head
- [ ] T013 [P] Seed ai_agents table with initial agents (maintenance_prophet, pricing_strategist) via migration or script
- [ ] T014 [P] Create Organization Pydantic schemas (Create, Read, Update) in apps/api/app/core/schemas/organization.py
- [ ] T015 [P] Create Store Pydantic schemas (Create, Read, Update) in apps/api/app/core/schemas/store.py
- [ ] T016 [P] Create IoT Controller Pydantic schemas (Create, Read, Update) in apps/api/app/core/schemas/iot_controller.py
- [ ] T017 [P] Create Agent Configuration Pydantic schemas (Read, Update) in apps/api/app/core/schemas/agent_configuration.py
- [ ] T018 [P] Create AI Agent Pydantic schemas (Read) in apps/api/app/core/schemas/ai_agent.py
- [ ] T018a [P] Create Invitation Pydantic schemas (Create, Read, Validate, Accept) in apps/api/app/core/schemas/invitation.py
- [ ] T019 [P] Create Organization repository implementing Repository protocol in apps/api/app/core/repositories/organization_repository.py
- [ ] T020 [P] Create Store repository implementing Repository protocol in apps/api/app/core/repositories/store_repository.py
- [ ] T021 [P] Create IoT Controller repository implementing Repository protocol in apps/api/app/core/repositories/iot_controller_repository.py
- [ ] T022 [P] Create Agent Configuration repository implementing Repository protocol in apps/api/app/core/repositories/agent_configuration_repository.py
- [ ] T022a [P] Extend User SQLAlchemy model with is_support_agent and is_provisioning_specialist boolean fields in apps/api/app/core/models/user.py
- [ ] T022b [P] Update User Pydantic schemas to include is_support_agent and is_provisioning_specialist fields in apps/api/app/core/schemas/user.py
- [ ] T022c [P] Create helper functions is_support_agent and is_provisioning_specialist in apps/api/app/auth/security.py
- [ ] T023 Extend auth decorators with require_support_agent and require_provisioning_specialist decorators in apps/api/app/auth/decorators.py
- [ ] T023a [P] Add unit tests for require_support_agent decorator in apps/api/tests/unit/utilities/test_decorators.py
- [ ] T023b [P] Add unit tests for require_provisioning_specialist decorator in apps/api/tests/unit/utilities/test_decorators.py
- [ ] T023c [P] Add unit tests for is_support_agent and is_provisioning_specialist helper functions in apps/api/tests/unit/domain/test_auth.py
- [ ] T024 [P] Add Organization, Store, IoT Controller, Agent Configuration, AI Agent TypeScript interfaces to packages/types/src/index.ts
- [ ] T025 [P] Setup React Query QueryClient provider in apps/web/src/app/layout.tsx or create providers directory

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Organization and Store Onboarding (Priority: P1) 🎯 MVP

**Goal**: Enable internal staff to create new customer organizations and stores through an onboarding wizard, then invite store owners to access their dashboard.

**Independent Test**: Create a new organization with one store and verify the store owner invitation email is sent. This delivers value by enabling new customer onboarding.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T026 [P] [US1] Unit test for Organization model creation and validation in apps/api/tests/unit/database/test_models_organization.py
- [ ] T027 [P] [US1] Unit test for Store model creation and validation in apps/api/tests/unit/database/test_models_store.py
- [ ] T027a [P] [US1] Unit test for Invitation model creation and validation in apps/api/tests/unit/database/test_models_invitation.py
- [ ] T027b [P] [US1] Unit test for User-Store association model in apps/api/tests/unit/database/test_models_user_store.py
- [ ] T027c [P] Unit test for User model with new role fields (is_support_agent, is_provisioning_specialist) in apps/api/tests/unit/database/test_models_user.py
- [ ] T028 [P] [US1] Unit test for Organization repository CRUD operations in apps/api/tests/unit/domain/test_organizations.py
- [ ] T029 [P] [US1] Unit test for Store repository CRUD operations in apps/api/tests/unit/domain/test_stores.py
- [ ] T030 [P] [US1] Integration test for POST /super-admin/organizations endpoint in apps/api/tests/integration/test_organizations_routes.py
- [ ] T031 [P] [US1] Integration test for GET /super-admin/organizations endpoint in apps/api/tests/integration/test_organizations_routes.py
- [ ] T032 [P] [US1] Integration test for POST /super-admin/organizations/{id}/stores endpoint in apps/api/tests/integration/test_stores_routes.py
- [ ] T033 [P] [US1] Integration test for POST /super-admin/stores/{id}/invite-owner endpoint in apps/api/tests/integration/test_stores_routes.py
- [ ] T033a [P] [US1] Integration test for GET /auth/invitations/{token}/validate endpoint in apps/api/tests/integration/test_invitations_routes.py
- [ ] T033b [P] [US1] Integration test for POST /auth/invitations/{token}/accept endpoint in apps/api/tests/integration/test_invitations_routes.py
- [ ] T033c [P] [US1] Unit test for invitation token generation in apps/api/tests/unit/domain/test_invitations.py
- [ ] T033d [P] [US1] Unit test for invitation expiration logic in apps/api/tests/unit/domain/test_invitations.py
- [ ] T033e [P] [US1] Unit test for email service in apps/api/tests/unit/domain/test_email_service.py

### Implementation for User Story 1

- [ ] T034 [US1] Create Organization router with GET /super-admin/organizations and POST /super-admin/organizations endpoints in apps/api/app/organizations/router.py
- [ ] T035 [US1] Create Organization router with GET /super-admin/organizations/{id} and PUT /super-admin/organizations/{id} endpoints in apps/api/app/organizations/router.py
- [ ] T036 [US1] Create Store router with GET /super-admin/organizations/{id}/stores and POST /super-admin/organizations/{id}/stores endpoints in apps/api/app/stores/router.py
- [ ] T037 [US1] Create Store router with GET /super-admin/stores/{id} and PUT /super-admin/stores/{id} endpoints in apps/api/app/stores/router.py
- [ ] T038b [P] [US1] Create invitation token generation utility function in apps/api/app/auth/invitation.py using secrets.token_urlsafe(32)
- [ ] T038c [P] [US1] Create email service utility using SendGrid in apps/api/app/core/services/email_service.py with send_invitation_email function
- [ ] T038d [US1] Create invitation acceptance endpoint POST /auth/invitations/{token}/accept in apps/api/app/auth/router.py
- [ ] T038e [US1] Create invitation validation endpoint GET /auth/invitations/{token}/validate in apps/api/app/auth/router.py
- [ ] T038f [P] [US1] Create email templates for store owner invitations (HTML and plain text) in apps/api/app/core/templates/invitation_email.html and invitation_email.txt
- [ ] T038g [US1] Implement store owner invitation endpoint POST /super-admin/stores/{id}/invite-owner in apps/api/app/stores/router.py with token generation, email sending, and invitation creation
- [ ] T038i [US1] Add invitation expiration check logic (automatic expiration on validation)
- [ ] T038j [US1] Add error handling for invitation edge cases (expired, already accepted, invalid token, duplicate email)
- [ ] T039 [US1] Register organizations and stores routers in apps/api/app/main.py
- [ ] T040 [US1] Create organization API client functions (list, get, create, update) in apps/web/src/features/organizations/api/client.ts
- [ ] T041 [US1] Create store API client functions (list, get, create, update, inviteOwner) in apps/web/src/features/stores/api/client.ts
- [ ] T042 [US1] Create organization React Query queries in apps/web/src/features/organizations/api/queries.ts
- [ ] T043 [US1] Create organization React Query mutations in apps/web/src/features/organizations/api/mutations.ts
- [ ] T044 [US1] Create store React Query queries in apps/web/src/features/stores/api/queries.ts
- [ ] T045 [US1] Create store React Query mutations in apps/web/src/features/stores/api/mutations.ts
- [ ] T046 [US1] Create useOrganizations and useOrganization custom hooks in apps/web/src/features/organizations/hooks/useOrganizations.ts
- [ ] T047 [US1] Create useStores and useStore custom hooks in apps/web/src/features/stores/hooks/useStores.ts
- [ ] T048 [US1] Create OrganizationWizard component for onboarding flow in apps/web/src/components/admin/OrganizationWizard.tsx
- [ ] T049 [US1] Create OrganizationList component in apps/web/src/components/admin/OrganizationList.tsx
- [ ] T050 [US1] Create OrganizationDetail page component in apps/web/src/app/super-admin/organizations/[id]/page.tsx
- [ ] T051 [US1] Create OrganizationList page (Server Component) in apps/web/src/app/super-admin/organizations/page.tsx
- [ ] T052 [US1] Create OrganizationCreate page (onboarding wizard) in apps/web/src/app/super-admin/organizations/new/page.tsx
- [ ] T053 [US1] Create StoreList component in apps/web/src/components/admin/StoreList.tsx
- [ ] T054 [US1] Create StoreCreate page in apps/web/src/app/super-admin/stores/new/page.tsx
- [ ] T055 [US1] Create StoreDetail page in apps/web/src/app/super-admin/stores/[id]/page.tsx
- [ ] T056 [US1] Create Next.js API route handlers for organizations in apps/web/src/app/api/super-admin/organizations/route.ts and apps/web/src/app/api/super-admin/organizations/[id]/route.ts
- [ ] T057 [US1] Create Next.js API route handlers for stores in apps/web/src/app/api/super-admin/stores/route.ts and apps/web/src/app/api/super-admin/stores/[id]/route.ts
- [ ] T058 [US1] Create Next.js API route handler for store owner invitation in apps/web/src/app/api/super-admin/stores/[id]/invite-owner/route.ts
- [ ] T058a [US1] Create frontend invitation acceptance page in apps/web/src/app/auth/accept-invitation/page.tsx with token validation and password setting form
- [ ] T058b [US1] Create invitation API client functions (validate, accept) in apps/web/src/features/invitations/api/client.ts
- [ ] T058c [US1] Create invitation React Query mutations in apps/web/src/features/invitations/api/mutations.ts
- [ ] T059 [US1] Add validation and error handling for organization and store creation
- [ ] T060 [US1] Add logging for organization and store operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Internal staff can create organizations, add stores, and invite store owners.

---

## Phase 4: User Story 2 - IoT Machine Mapping (Priority: P2)

**Goal**: Enable provisioning specialists to map physical IoT controller devices (identified by MAC addresses or serial numbers) to logical machine labels that appear in the operator's dashboard.

**Independent Test**: Provision a controller with MAC address "AA:BB:CC:DD:EE:FF" and map it to "Washer #1", then verify the mapping is stored correctly. This delivers value by enabling IoT device connectivity and monitoring.

### Tests for User Story 2 ⚠️

- [ ] T061 [P] [US2] Unit test for IoT Controller model creation and validation in apps/api/tests/unit/database/test_models_iot_controller.py
- [ ] T062 [P] [US2] Unit test for IoT Controller repository CRUD operations in apps/api/tests/unit/domain/test_iot_mapping.py
- [ ] T063 [P] [US2] Integration test for GET /super-admin/stores/{id}/iot endpoint in apps/api/tests/integration/test_iot_routes.py
- [ ] T064 [P] [US2] Integration test for POST /super-admin/stores/{id}/iot endpoint in apps/api/tests/integration/test_iot_routes.py
- [ ] T065 [P] [US2] Integration test for PUT /super-admin/stores/{id}/iot/{controller_id} endpoint in apps/api/tests/integration/test_iot_routes.py
- [ ] T066 [P] [US2] Integration test for DELETE /super-admin/stores/{id}/iot/{controller_id} endpoint in apps/api/tests/integration/test_iot_routes.py

### Implementation for User Story 2

- [ ] T067 [US2] Create IoT router with GET /super-admin/stores/{id}/iot endpoint in apps/api/app/iot/router.py
- [ ] T068 [US2] Create IoT router with POST /super-admin/stores/{id}/iot endpoint in apps/api/app/iot/router.py
- [ ] T069 [US2] Create IoT router with PUT /super-admin/stores/{id}/iot/{controller_id} endpoint in apps/api/app/iot/router.py
- [ ] T070 [US2] Create IoT router with DELETE /super-admin/stores/{id}/iot/{controller_id} endpoint in apps/api/app/iot/router.py
- [ ] T071 [US2] Register IoT router in apps/api/app/main.py
- [ ] T072 [US2] Create IoT controller API client functions (list, get, create, update, delete) in apps/web/src/features/iot/api/client.ts
- [ ] T073 [US2] Create IoT controller React Query queries in apps/web/src/features/iot/api/queries.ts
- [ ] T074 [US2] Create IoT controller React Query mutations in apps/web/src/features/iot/api/mutations.ts
- [ ] T075 [US2] Create useIoTControllers custom hook in apps/web/src/features/iot/hooks/useIoTControllers.ts
- [ ] T076 [US2] Create IoTMappingTable component in apps/web/src/components/admin/IoTMappingTable.tsx
- [ ] T077 [US2] Create IoT mapping page in apps/web/src/app/super-admin/stores/[id]/iot/page.tsx
- [ ] T078 [US2] Create Next.js API route handlers for IoT controllers in apps/web/src/app/api/super-admin/stores/[id]/iot/route.ts and apps/web/src/app/api/super-admin/stores/[id]/iot/[controllerId]/route.ts
- [ ] T079 [US2] Add MAC address format validation (regex: ^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$)
- [ ] T080 [US2] Add validation for unique MAC addresses and serial numbers per store
- [ ] T081 [US2] Add error handling and logging for IoT controller operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Provisioning specialists can map IoT controllers to machine labels.

---

## Phase 5: User Story 3 - Agent Subscription Management (Priority: P2)

**Goal**: Enable Super-Admins to enable or disable AI agents (e.g., Maintenance Prophet, Pricing Strategist) for each store based on their subscription tier, controlling which agentic features are available.

**Independent Test**: Enable "Maintenance Prophet" for Store A and disable it for Store B, then verify Store A's operator can access maintenance features while Store B's operator cannot. This delivers value by enabling subscription-based feature access.

### Tests for User Story 3 ⚠️

- [ ] T082 [P] [US3] Unit test for Agent Configuration model creation and validation in apps/api/tests/unit/database/test_models_agent_configuration.py
- [ ] T083 [P] [US3] Unit test for Agent Configuration repository CRUD operations in apps/api/tests/unit/domain/test_agent_configuration.py
- [ ] T084 [P] [US3] Integration test for GET /super-admin/stores/{id}/agents endpoint in apps/api/tests/integration/test_agents_routes.py
- [ ] T085 [P] [US3] Integration test for PUT /super-admin/stores/{id}/agents endpoint in apps/api/tests/integration/test_agents_routes.py

### Implementation for User Story 3

- [ ] T086 [US3] Create Agents router with GET /super-admin/stores/{id}/agents endpoint in apps/api/app/agents/router.py
- [ ] T087 [US3] Create Agents router with PUT /super-admin/stores/{id}/agents endpoint in apps/api/app/agents/router.py
- [ ] T088 [US3] Register agents router in apps/api/app/main.py
- [ ] T089 [US3] Create agent configuration API client functions (get, update) in apps/web/src/features/agents/api/client.ts
- [ ] T090 [US3] Create agent configuration React Query queries in apps/web/src/features/agents/api/queries.ts
- [ ] T091 [US3] Create agent configuration React Query mutations in apps/web/src/features/agents/api/mutations.ts
- [ ] T092 [US3] Create useAgentConfiguration custom hook in apps/web/src/features/agents/hooks/useAgentConfiguration.ts
- [ ] T093 [US3] Create AgentConfiguration component with toggle switches in apps/web/src/components/admin/AgentConfiguration.tsx
- [ ] T094 [US3] Create agent configuration page in apps/web/src/app/super-admin/stores/[id]/agents/page.tsx
- [ ] T095 [US3] Create Next.js API route handlers for agent configuration in apps/web/src/app/api/super-admin/stores/[id]/agents/route.ts
- [ ] T096 [US3] Add validation for enabled_agents array (must contain valid AI agent identifiers)
- [ ] T097 [US3] Add error handling and logging for agent configuration operations
- [ ] T098 [US3] Implement immediate effect of agent configuration changes (cache invalidation)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Super-Admins can manage agent subscriptions per store.

---

## Phase 6: User Story 4 - System Health Monitoring (Priority: P2)

**Goal**: Enable internal staff to monitor the health status of all stores, including IoT connectivity, device status, and system alerts, to proactively identify and resolve operational issues.

**Independent Test**: View the global IoT pulse dashboard and verify that online stores show green status while offline stores show red status with alert indicators. This delivers value by enabling proactive system monitoring and issue resolution.

### Tests for User Story 4 ⚠️

- [ ] T099 [P] [US4] Unit test for System Health Status calculation logic in apps/api/tests/unit/domain/test_health_monitoring.py
- [ ] T100 [P] [US4] Integration test for GET /super-admin/health endpoint in apps/api/tests/integration/test_health_routes.py

### Implementation for User Story 4

- [ ] T101 [US4] Create Health router with GET /super-admin/health endpoint in apps/api/app/health/router.py
- [ ] T102 [US4] Implement System Health Status calculation logic (aggregate IoT controller statuses per store) in apps/api/app/health/router.py
- [ ] T103 [US4] Register health router in apps/api/app/main.py
- [ ] T104 [US4] Create system health API client function (get) in apps/web/src/features/health/api/client.ts
- [ ] T105 [US4] Create system health React Query queries in apps/web/src/features/health/api/queries.ts
- [ ] T106 [US4] Create useSystemHealth custom hook in apps/web/src/features/health/hooks/useSystemHealth.ts
- [ ] T107 [US4] Create HealthDashboard component with status indicators and alerts in apps/web/src/components/admin/HealthDashboard.tsx
- [ ] T108 [US4] Create system health dashboard page in apps/web/src/app/super-admin/health/page.tsx
- [ ] T109 [US4] Create Next.js API route handler for system health in apps/web/src/app/api/super-admin/health/route.ts
- [ ] T110 [US4] Implement 30-second polling for health status updates in HealthDashboard component
- [ ] T111 [US4] Add filtering and searching by organization name, store name, status, or location
- [ ] T112 [US4] Add alert indicators for offline stores (>2 minutes = alert, >5 minutes = critical)
- [ ] T113 [US4] Add error handling and logging for health monitoring operations

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently. Internal staff can monitor system health across all stores.

---

## Phase 7: User Story 5 - Shadow View (View as Operator) (Priority: P3)

**Goal**: Enable Support Agents to view a store's operator dashboard exactly as the operator sees it, to troubleshoot issues and provide accurate support guidance.

**Independent Test**: A Support Agent selects "View as Operator" for a specific store and verifies the dashboard displays exactly as the operator would see it, with the same data, layout, and available actions. This delivers value by enabling accurate troubleshooting and support.

### Tests for User Story 5 ⚠️

- [ ] T114 [P] [US5] Integration test for Shadow View read-only access enforcement in apps/api/tests/integration/test_shadow_view.py
- [ ] T115 [P] [US5] Integration test for Shadow View audit logging in apps/api/tests/integration/test_shadow_view.py

### Implementation for User Story 5

- [ ] T116 [US5] Create Shadow View page component in apps/web/src/app/super-admin/shadow-view/[storeId]/page.tsx
- [ ] T117 [US5] Create ShadowView component that renders operator dashboard in read-only mode in apps/web/src/components/admin/ShadowView.tsx
- [ ] T118 [US5] Implement read-only mode enforcement (disable all mutation actions) in ShadowView component
- [ ] T119 [US5] Create audit logging middleware for Shadow View actions in apps/api/app/auth/decorators.py or separate middleware
- [ ] T120 [US5] Add "shadow_view" indicator to all logged actions (user, timestamp, action type)
- [ ] T121 [US5] Add error message display when user attempts to modify data in Shadow View mode
- [ ] T122 [US5] Ensure multiple Support Agents can use Shadow View simultaneously without interference
- [ ] T123 [US5] Add error handling and logging for Shadow View operations

**Checkpoint**: All user stories should now be independently functional. Support Agents can troubleshoot operator issues using Shadow View.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T124 [P] Add password reset functionality for Support Agents (POST /super-admin/users/{id}/reset-password) in apps/api/app/users/router.py
- [ ] T125 [P] Create password reset API client function and hook in apps/web/src/features/users/api/client.ts and hooks/useUserManagement.ts
- [ ] T126 [P] Add password reset UI component in apps/web/src/components/admin/UserManagement.tsx
- [ ] T127 [P] Update super-admin landing page to include navigation to all new features in apps/web/src/app/super-admin/page.tsx
- [ ] T128 [P] Add role-based access control checks to all frontend routes (Super-Admin, Support Agent, Provisioning Specialist)
- [ ] T129 [P] Add comprehensive error boundaries and error handling across all components
- [ ] T130 [P] Add loading states and skeleton loaders for all data fetching operations
- [ ] T131 [P] Optimize database queries with proper indexes (verify indexes from data-model.md are created)
- [ ] T132 [P] Add pagination support to all list endpoints and UI components
- [ ] T133 [P] Add search and filter functionality to organization and store lists
- [ ] T134 [P] Add accessibility (a11y) improvements: ARIA labels, keyboard navigation, semantic HTML
- [ ] T135 [P] Add responsive design improvements for tablet and mobile views
- [ ] T136 [P] Performance optimization: code splitting for dashboard routes, lazy loading components
- [ ] T137 [P] Add comprehensive logging for all critical operations (onboarding, IoT mapping, agent configuration)
- [ ] T138 [P] Security hardening: validate all inputs, sanitize outputs, add rate limiting if needed
- [ ] T139 [P] Documentation updates: API documentation, component documentation, user guides
- [ ] T140 [P] Run quickstart.md validation to ensure all setup steps work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires Store entity from US1, but can work with minimal Store implementation
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Requires Store entity from US1, but can work with minimal Store implementation
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Requires Store and IoT Controller entities from US1 and US2, but can work with minimal implementations
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Requires Store entity from US1, but can work with minimal Store implementation

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before repositories
- Repositories before routers
- Backend routers before frontend API clients
- API clients before React Query queries/mutations
- React Query setup before custom hooks
- Custom hooks before components
- Components before pages
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Frontend and backend work can proceed in parallel once API contracts are defined

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Organization model creation and validation in apps/api/tests/unit/database/test_models_organization.py"
Task: "Unit test for Store model creation and validation in apps/api/tests/unit/database/test_models_store.py"
Task: "Unit test for Organization repository CRUD operations in apps/api/tests/unit/domain/test_organizations.py"
Task: "Unit test for Store repository CRUD operations in apps/api/tests/unit/domain/test_stores.py"

# Launch all API client functions together:
Task: "Create organization API client functions (list, get, create, update) in apps/web/src/features/organizations/api/client.ts"
Task: "Create store API client functions (list, get, create, update, inviteOwner) in apps/web/src/features/stores/api/client.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Organizations & Stores)
   - Developer B: User Story 2 (IoT Mapping) - can start after US1 Store model is done
   - Developer C: User Story 3 (Agent Configuration) - can start after US1 Store model is done
3. After US1-3 complete:
   - Developer A: User Story 4 (Health Monitoring)
   - Developer B: User Story 5 (Shadow View)
   - Developer C: Polish & Cross-Cutting Concerns
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Follow constitution requirements: type safety, testing discipline, performance targets
- Use existing patterns: Repository pattern, dependency injection, Pydantic validation
- Frontend: React Query for server state, useState for UI state, Server Components by default

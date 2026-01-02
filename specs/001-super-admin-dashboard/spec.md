# Feature Specification: Super-User Admin Dashboard (Control Room)

**Feature Branch**: `001-super-admin-dashboard`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "PRD: Laundromaid Super-User Admin Dashboard (The \"Control Room\")"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organization and Store Onboarding (Priority: P1)

Internal staff need to create new customer organizations and their physical store locations through a guided onboarding wizard, then invite organization members to access their dashboard.

**Why this priority**: Without this capability, new customers cannot be onboarded. This is the foundational workflow that enables all other operations. The system cannot provision new stores without this feature.

**Independent Test**: Can be fully tested by creating a new organization with one store and verifying the organization member invitation email is sent. Delivers value by enabling new customer onboarding.

**Acceptance Scenarios**:

1. **Given** a Super-Admin is logged into the Control Room, **When** they complete the onboarding wizard to create an organization named "Sunny Laundromat LLC" with address "123 Main St", **Then** the organization is created and stored in the system.
2. **Given** an organization exists, **When** a Super-Admin adds a new store location "Downtown Branch" with address "456 Oak Ave", **Then** the store is associated with the organization and displayed in the organization's store list.
3. **Given** an organization has been created, **When** a Super-Admin invites an organization member by entering their email address "dan@example.com" and selecting a role (owner, employee, or admin), **Then** an invitation email is sent and the user account is created with the specified role for that organization.
4. **Given** an organization member invitation has been sent, **When** the member clicks the invitation link, **Then** they are prompted to set a password and granted access to their organization dashboard with access to all stores in the organization.

---

### User Story 2 - IoT Machine Mapping (Priority: P2)

Provisioning specialists need to map physical IoT controller devices (identified by MAC addresses or serial numbers) to logical machine labels (e.g., "Washer #1") that appear in the operator's dashboard.

**Why this priority**: Hardware-to-software mapping is required for IoT integration. Operators need to see which physical machines correspond to which digital labels. This must be completed during store setup before the store can operate with IoT monitoring.

**Independent Test**: Can be fully tested by provisioning a controller with MAC address "AA:BB:CC:DD:EE:FF" and mapping it to "Washer #1", then verifying the mapping is stored correctly. Delivers value by enabling IoT device connectivity and monitoring.

**Acceptance Scenarios**:

1. **Given** a store exists, **When** a Provisioning Specialist enters a controller MAC address "AA:BB:CC:DD:EE:FF" and maps it to label "Washer #1", **Then** the mapping is saved and the controller is associated with that store.
2. **Given** multiple controllers are provisioned for a store, **When** a Provisioning Specialist views the machine mapping table, **Then** all controllers are displayed with their MAC addresses, serial numbers, and assigned labels.
3. **Given** a controller mapping exists, **When** a Provisioning Specialist updates the label from "Washer #1" to "Front Washer #1", **Then** the label change is saved and reflected in the operator's dashboard.
4. **Given** a controller is mapped to a machine, **When** the operator views their dashboard, **Then** the machine appears with the assigned label and IoT connectivity status.

---

### User Story 3 - Agent Subscription Management (Priority: P2)

Super-Admins need to enable or disable AI agents (e.g., Maintenance Prophet, Pricing Strategist) for each store based on their subscription tier, controlling which agentic features are available.

**Why this priority**: Subscription management directly impacts revenue and customer experience. Different customers pay for different agent tiers, so the system must enforce feature access based on contracts. This is required for billing accuracy and feature access control.

**Independent Test**: Can be fully tested by enabling "Maintenance Prophet" for Store A and disabling it for Store B, then verifying Store A's operator can access maintenance features while Store B's operator cannot. Delivers value by enabling subscription-based feature access.

**Acceptance Scenarios**:

1. **Given** a store exists, **When** a Super-Admin toggles "Maintenance Prophet" to enabled, **Then** the agent is activated for that store and operators can access maintenance prediction features.
2. **Given** multiple AI agents exist in the system, **When** a Super-Admin views the agent configuration for a store, **Then** all available agents are displayed with their current enabled/disabled status.
3. **Given** an agent is disabled for a store, **When** an operator attempts to access features provided by that agent, **Then** they receive a message indicating the feature requires a subscription upgrade.
4. **Given** a store's subscription tier changes, **When** a Super-Admin updates the enabled agents list, **Then** the changes take effect immediately and operators' available features update accordingly.

---

### User Story 4 - System Health Monitoring (Priority: P2)

Internal staff need to monitor the health status of all stores, including IoT connectivity, device status, and system alerts, to proactively identify and resolve operational issues.

**Why this priority**: Operational reliability requires visibility into system health. When stores go offline or IoT devices fail, internal staff must be notified immediately to maintain service quality. This enables proactive support and reduces customer complaints.

**Independent Test**: Can be fully tested by viewing the global IoT pulse dashboard and verifying that online stores show green status while offline stores show red status with alert indicators. Delivers value by enabling proactive system monitoring and issue resolution.

**Acceptance Scenarios**:

1. **Given** multiple stores exist in the system, **When** a Super-Admin views the global IoT pulse dashboard, **Then** all stores are displayed with their current connectivity status (online/offline).
2. **Given** a store's IoT bridge goes offline, **When** the system detects the connectivity loss, **Then** an alert is displayed on the dashboard and the store's status changes to "Offline" with a timestamp.
3. **Given** stores with varying health statuses exist, **When** a Support Agent views the system health dashboard, **Then** stores are sorted by alert severity and offline stores appear at the top of the list.
4. **Given** a store has been offline for more than 5 minutes, **When** a Support Agent views the dashboard, **Then** the store is highlighted with a critical alert indicator and troubleshooting options are available.

---

### User Story 5 - Shadow View (View as Operator) (Priority: P3)

Support Agents need to view a store's operator dashboard exactly as the operator sees it, to troubleshoot issues and provide accurate support guidance.

**Why this priority**: Troubleshooting customer issues requires seeing the exact view the customer experiences. This reduces support resolution time and improves customer satisfaction. However, this can be deferred to P3 as support can work around it initially by having customers describe their view.

**Independent Test**: Can be fully tested by a Support Agent selecting "View as Operator" for a specific store and verifying the dashboard displays exactly as the operator would see it, with the same data, layout, and available actions. Delivers value by enabling accurate troubleshooting and support.

**Acceptance Scenarios**:

1. **Given** a Support Agent is viewing a store's details, **When** they click "View as Operator", **Then** the operator dashboard loads displaying the same data and interface the operator would see.
2. **Given** a Support Agent is in Shadow View mode, **When** they interact with the dashboard, **Then** all actions are logged with a "shadow view" indicator for audit purposes.
3. **Given** a Support Agent is viewing as operator, **When** they attempt to perform actions that modify data, **Then** the system prevents the action and displays a message that shadow view is read-only.
4. **Given** multiple Support Agents need to troubleshoot the same store, **When** they simultaneously use Shadow View, **Then** each agent sees an independent view without interfering with others.

---

### Edge Cases

- What happens when an organization member's email address is already in use by another user?
- How does the system handle duplicate MAC addresses or serial numbers during IoT provisioning?
- What happens when an organization has no stores created yet - can it exist?
- How does the system handle stores with no IoT controllers provisioned - do they appear in health monitoring?
- What happens when all agents are disabled for a store - what features remain accessible to operators?
- How does the system handle expired or invalid organization member invitations?
- What happens when an IoT controller is mapped to a machine that is later deleted?
- How does the system handle stores that have been deleted but still have active IoT controllers?
- What happens when a Support Agent tries to view as operator for a store they don't have permission to access?
- How does the system handle concurrent updates to agent configuration by multiple Super-Admins?
- How does the system handle organization members with different roles (owner, employee, admin) accessing stores?
- What happens when an organization is deleted but has active invitations pending?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an onboarding wizard that guides internal staff through creating an organization with required details (name, address, contact information).
- **FR-002**: System MUST allow creation of multiple store locations under a single organization, each with its own address and identifier.
- **FR-003**: System MUST support sending email invitations to organization members with secure invitation links that expire after a configurable time period (default: 7 days, configurable via `INVITATION_EXPIRATION_DAYS` environment variable).
- **FR-004**: System MUST enforce role-based access control with three distinct roles: Super-Admin (full access), Support Agent (read-only financial data, can reset passwords), and Provisioning Specialist (machine mapping and store setup). Roles are stored as boolean flags on the User model: `is_super_admin`, `is_support_agent`, `is_provisioning_specialist`.
- **FR-005**: System MUST allow provisioning of IoT controllers by MAC address or serial number, associating each controller with a specific store.
- **FR-006**: System MUST provide a mapping interface where physical IoT controllers can be assigned logical labels (e.g., "Washer #1", "Dryer #3") that appear in operator dashboards.
- **FR-007**: System MUST allow Super-Admins to enable or disable individual AI agents (e.g., Maintenance Prophet, Pricing Strategist) on a per-store basis.
- **FR-008**: System MUST display the current enabled/disabled status of all available AI agents for each store.
- **FR-009**: System MUST provide a global dashboard showing the connectivity status of all stores and their IoT bridges.
- **FR-010**: System MUST generate alerts when a store's IoT bridge goes offline or connectivity is lost.
- **FR-011**: System MUST provide a "Shadow View" feature that allows Support Agents to view a store's operator dashboard exactly as the operator would see it.
- **FR-012**: System MUST log all actions performed in Shadow View mode with audit trail information (user, timestamp, action type).
- **FR-013**: System MUST prevent data modifications when viewing in Shadow View mode (read-only access).
- **FR-014**: System MUST validate that MAC addresses and serial numbers are unique per store during IoT controller provisioning.
- **FR-015**: System MUST require organization member email addresses to be unique per organization (same email can belong to different organizations).
- **FR-016**: System MUST allow Support Agents to reset user passwords for organization members and store operators.
- **FR-017**: System MUST display machine mapping information (controller identifier, assigned label) in a searchable, sortable table format.
- **FR-018**: System MUST allow updating machine labels after initial provisioning without requiring controller re-provisioning.
- **FR-019**: System MUST display system health status in a high-density, data-rich interface optimized for internal staff use.
- **FR-020**: System MUST support filtering and searching stores by organization name, store name, status, or location in health monitoring views.

### Key Entities *(include if feature involves data)*

- **Organization**: Represents the parent company that owns one or more store locations. Attributes include name, billing address, contact information, and creation date. Relationships: has many Stores, has many Users via UserOrganization (organization-level members with roles: owner, employee, admin).

- **UserOrganization**: Represents the many-to-many relationship between Users and Organizations for organization-level access. Attributes include user_id, organization_id, role (enum: owner, employee, admin), and created_at. Relationships: belongs to one User, belongs to one Organization. Purpose: Organization-level users (via UserOrganization) have automatic access to all stores in their organization. Organization OWNER role provides full access to all stores; EMPLOYEE and ADMIN roles have access determined by organization admin (store assignments managed separately).

- **Store**: Represents a physical laundromat location. Attributes include name, street address, city, state, postal code, organization affiliation, status (active/inactive), and creation date. Relationships: belongs to one Organization, has many IoT Controllers, has many Users via UserStore (store owners/operators, for store-specific access), has Agent Configuration. Note: Organization-level users (via UserOrganization) have automatic access to all stores in their organization.

- **IoT Controller**: Represents a physical hardware device installed on a machine. Attributes include MAC address (unique identifier), serial number (optional unique identifier), store affiliation, machine label (logical name like "Washer #1" that appears in operator dashboards), provisioned date, and connectivity status. The `machine_label` is stored as a string field on the IoT Controller entity (not a separate table). Relationships: belongs to one Store.

- **Agent Configuration**: Represents the subscription/feature access settings for a store. Attributes include store affiliation, enabled agents list, and last updated timestamp. Relationships: belongs to one Store, references multiple AI Agents.

- **AI Agent**: Represents an available intelligent agent feature (e.g., Maintenance Prophet, Pricing Strategist). Attributes include agent name, description, and availability status. Relationships: can be enabled/disabled per Store via Agent Configuration.

- **System Health Status**: Represents the current operational state of a store's IoT infrastructure. Attributes include store affiliation, connectivity status (online/offline), last heartbeat timestamp, alert count, and device status summary. Relationships: belongs to one Store.

- **Invitation**: Represents an organization member invitation sent via email. Attributes include token (secure URL-safe token), email address, organization affiliation, organization_role (enum: owner, employee, admin), invited_by (User who sent invitation), status (pending/accepted/expired/revoked), expires_at, accepted_at, and creation timestamp. Relationships: belongs to one Organization, created by one User (invited_by), accepted by one User (when accepted).

## Invitation System Details

### Invitation Token Model

- **Token Generation**: Secure token generation using `secrets.token_urlsafe(32)` (32-byte token, URL-safe base64 encoding)
- **Token Storage**: Tokens stored in `invitations` table with expiration tracking and status management
- **Default Expiration**: 7 days from creation (configurable via `INVITATION_EXPIRATION_DAYS` environment variable)
- **Token Uniqueness**: Each token MUST be unique across all invitations (database unique constraint)

### Invitation Acceptance Flow

1. **User clicks invitation link**: `{FRONTEND_URL}/auth/accept-invitation?token={token}`
2. **Frontend validates token**: Calls `GET /auth/invitations/{token}/validate` to verify token is valid and not expired
3. **User sets password**: Submits password via `POST /auth/invitations/{token}/accept` with password field
4. **System creates User account**: If user with email doesn't exist, creates new User account with email
5. **System associates User with Organization**: Creates user-organization relationship via UserOrganization with specified role (owner, employee, or admin) from invitation's `organization_role` field
6. **System marks invitation as accepted**: Updates invitation status to "accepted" and sets `accepted_at` timestamp
7. **User is authenticated**: System logs user in and redirects to organization dashboard or portal

### Email Service Integration

- **Email Provider**: SendGrid (already in dependencies: `sendgrid==6.10.0`)
- **Required Environment Variables**:
  - `SENDGRID_API_KEY`: SendGrid API key for authentication
  - `FROM_EMAIL`: Sender email address (e.g., "noreply@laundromate.com")
  - `FRONTEND_URL`: Base URL for frontend application (e.g., "https://app.laundromate.com")
- **Email Service Utility**: Centralized email service in `apps/api/app/core/services/email_service.py`
- **Error Handling**: Failed email sends MUST be logged; retry logic for transient failures (3 retries with exponential backoff)
- **Email Delivery Tracking**: Log email delivery status (sent, delivered, failed) for audit purposes

### Email Template Requirements

- **Subject Line**: "You've been invited to manage {Organization Name} on LaundroMate"
- **Email Body Content**:
  - Organization name
  - Role information (owner, employee, or admin)
  - Invitation link (full URL with token parameter)
  - Expiration notice (e.g., "This invitation expires in 7 days")
  - Instructions for accepting invitation
  - Support contact information
- **Format**: Both HTML and plain text versions MUST be provided
- **Branding**: Email MUST be branded with LaundroMate styling and logo
- **Template Location**: `apps/api/app/core/templates/invitation_email.html` (HTML) and `.txt` (plain text)

### Invitation Status & Lifecycle

- **Status Enum**: `pending`, `accepted`, `expired`, `revoked`
- **State Transitions**:
  - `pending` → `accepted`: When user successfully accepts invitation
  - `pending` → `expired`: When `expires_at` timestamp passes (checked on validation)
  - `pending` → `revoked`: When Super-Admin manually revokes invitation
  - `accepted`, `expired`, `revoked` → (no further transitions, terminal states)
- **Automatic Expiration**: Expiration checked on token validation; expired invitations return 410 Gone status
- **Revocation**: Super-Admin can revoke pending invitations via `DELETE /super-admin/invitations/{id}` endpoint

### Resend Functionality

- **Idempotent Behavior**: If a pending invitation exists for the same email and organization, the system MAY resend the existing invitation email (same token) OR generate a new invitation (invalidating the old one)
- **Recommended Approach**: Generate new invitation token when resending, invalidating old invitation to prevent confusion
- **Resend Endpoint**: `POST /super-admin/organizations/{id}/resend-invitation` with email parameter (optional, defaults to most recent invitation for that organization)

### User Creation & Permissions

- **User Creation**: When invitation is accepted, if User with email doesn't exist, create new User with:
  - `email`: From invitation
  - `is_active`: `true`
  - `is_admin`: `false` (unless explicitly set)
  - `is_super_admin`: `false`
- **Organization Association**: Create user-organization relationship (many-to-many if users can belong to multiple organizations):
  - Table: `user_organizations` with columns: `user_id`, `organization_id`, `role` (enum: owner, employee, admin), `created_at`
  - Role: Set from invitation's `organization_role` field
- **Permission Model**:
  - Organization OWNER role: Full access to all stores in the organization
  - Organization EMPLOYEE/ADMIN roles: Access determined by organization admin (store assignments managed separately)
  - Store-level users (via UserStore): Specific to individual stores for store-specific operators

### Error Handling & Edge Cases

- **Expired Invitations**: Return `410 Gone` with message: "This invitation has expired. Please request a new invitation."
- **Already Accepted**: Return `400 Bad Request` with message: "This invitation has already been used."
- **Invalid Token**: Return `404 Not Found` with message: "Invitation not found."
- **Email Already Exists**:
  - If user exists but not associated with organization: Associate existing user with organization via UserOrganization and mark invitation as accepted
  - If user exists and already associated with organization: Return `409 Conflict` with message: "User is already a member of this organization."
- **Organization Deleted**: If organization is deleted after invitation sent, return `404 Not Found` with message: "Organization no longer exists."
- **Invalid Email Format**: Return `400 Bad Request` with validation error during invitation creation
- **Duplicate Invitation**: If pending invitation exists for same email/organization, return `409 Conflict` with option to resend

### Frontend Acceptance Flow

- **Page Route**: `/auth/accept-invitation?token={token}`
- **Token Validation**: On page load, call `GET /auth/invitations/{token}/validate` to check token validity
- **Loading States**: Display loading state while validating token
- **Error States**: Display appropriate error messages for expired, invalid, or already-accepted invitations
- **Password Form**: Once token validated, display password setting form with:
  - Password field (with strength indicator)
  - Confirm password field
  - Submit button
- **Success State**: After successful acceptance, display success message and redirect to organization dashboard or portal
- **Redirect Logic**: After acceptance, redirect to `/portal` or organization dashboard

### Audit Trail

- **Invitation Creation**: Log `invited_by` (User who sent invitation), `created_at`, `email`, `organization_id`, `organization_role`
- **Invitation Acceptance**: Log `accepted_at`, `accepted_by` (User who accepted), `user_id` (created or existing)
- **Invitation Revocation**: Log `revoked_at`, `revoked_by` (Super-Admin who revoked)
- **All Events**: Store in invitation model and optionally in audit log table for compliance

## Role-Based Access Control (RBAC) Details

### Role Model

The system uses boolean flags on the User model to represent internal staff roles. This approach is simpler than a separate role table for internal staff, as these roles are mutually exclusive and rarely change.

**User Model Fields**:
- `is_super_admin` (Boolean, existing): Full access to all features
- `is_support_agent` (Boolean, new): Support and troubleshooting access
- `is_provisioning_specialist` (Boolean, new): Machine mapping and store setup access

**Role Mutually Exclusive**: A user SHOULD have only one of these internal staff roles set to `true`. If multiple are set, `is_super_admin` takes precedence.

### Role Definitions & Permissions

#### Super-Admin
- **Full Access**: Can perform all operations in the Control Room
- **Permissions**:
  - Create, read, update, delete organizations and stores
  - Invite organization members (with roles: owner, employee, admin)
  - Configure IoT controllers and machine mappings
  - Enable/disable AI agents for stores
  - View system health dashboard
  - Use Shadow View
  - Reset user passwords
  - Revoke invitations
  - Access financial data (full read/write)
- **Use Case**: Internal operations managers, system administrators

#### Support Agent
- **Limited Access**: Focused on support and troubleshooting
- **Permissions**:
  - **Read-only** access to organizations and stores (view details, list)
  - **Read-only** access to financial data (cannot modify billing, pricing)
  - View system health dashboard
  - Use Shadow View to troubleshoot operator issues
  - Reset user passwords for organization members and store operators
  - View IoT controller status and machine mappings (read-only)
  - View agent configurations (read-only)
- **Restrictions**:
  - Cannot create or modify organizations/stores
  - Cannot provision IoT controllers or modify machine mappings
  - Cannot modify agent configurations
  - Cannot invite organization members
  - Cannot access financial modification features
- **Use Case**: Customer support staff, help desk operators

#### Provisioning Specialist
- **Focused Access**: Machine mapping and initial store setup
- **Permissions**:
  - Create and update stores (within organizations)
  - Provision IoT controllers (create, update, delete)
  - Map machine labels to IoT controllers
  - View store details and IoT mappings
  - View system health dashboard (read-only)
- **Restrictions**:
  - Cannot create organizations
  - Cannot invite organization members
  - Cannot modify agent configurations
  - Cannot use Shadow View
  - Cannot reset passwords
  - Cannot access financial data
  - Cannot modify organization details
- **Use Case**: Field technicians, hardware installation staff

### Role Assignment

- **Super-Admin Assignment**: Only existing Super-Admins can assign Super-Admin role to other users
- **Support Agent Assignment**: Super-Admins can assign Support Agent role
- **Provisioning Specialist Assignment**: Super-Admins can assign Provisioning Specialist role
- **Role Changes**: Super-Admins can modify roles of other users; users cannot modify their own roles

### Authorization Decorators

The system provides decorators for role-based authorization:

- `@require_super_admin`: Requires `is_super_admin = True`
- `@require_support_agent`: Requires `is_support_agent = True` OR `is_super_admin = True` (Super-Admins have all permissions)
- `@require_provisioning_specialist`: Requires `is_provisioning_specialist = True` OR `is_super_admin = True`
- `@require_admin`: Existing decorator (requires `is_admin = True` OR `is_super_admin = True`)

**Permission Hierarchy**: Super-Admins automatically have all permissions granted to Support Agents and Provisioning Specialists. Decorators should check Super-Admin status first, then role-specific status.

### Helper Functions

Utility functions in `apps/api/app/auth/security.py`:

- `is_super_admin(user: User) -> bool`: Check if user is Super-Admin (existing)
- `is_support_agent(user: User) -> bool`: Check if user is Support Agent or Super-Admin
- `is_provisioning_specialist(user: User) -> bool`: Check if user is Provisioning Specialist or Super-Admin
- `has_role(user: User, role: str) -> bool`: Generic role checker (role: "super_admin", "support_agent", "provisioning_specialist")

### Permission Matrix

| Feature | Super-Admin | Support Agent | Provisioning Specialist |
|---------|-------------|---------------|-------------------------|
| Create Organization | ✅ | ❌ | ❌ |
| View Organizations | ✅ | ✅ (read-only) | ✅ (read-only) |
| Update Organization | ✅ | ❌ | ❌ |
| Create Store | ✅ | ❌ | ✅ |
| View Stores | ✅ | ✅ (read-only) | ✅ |
| Update Store | ✅ | ❌ | ✅ |
| Invite Organization Member | ✅ | ❌ | ❌ |
| Provision IoT Controllers | ✅ | ❌ | ✅ |
| View IoT Mappings | ✅ | ✅ (read-only) | ✅ |
| Update Machine Labels | ✅ | ❌ | ✅ |
| Configure AI Agents | ✅ | ❌ | ❌ |
| View Agent Config | ✅ | ✅ (read-only) | ❌ |
| View System Health | ✅ | ✅ | ✅ |
| Shadow View | ✅ | ✅ | ❌ |
| Reset Passwords | ✅ | ✅ | ❌ |
| View Financial Data | ✅ | ✅ (read-only) | ❌ |
| Modify Financial Data | ✅ | ❌ | ❌ |

### Database Migration

- **New Fields**: Add `is_support_agent` and `is_provisioning_specialist` boolean columns to `users` table
- **Default Values**: Both fields default to `False`
- **Nullable**: Both fields are `NOT NULL` with default `False`
- **Indexes**: Consider adding indexes if role-based queries are frequent (optional optimization)

### Frontend Role Checks

- **Route Protection**: Frontend routes MUST check user roles before rendering
- **Component-Level**: Components can conditionally render features based on user role
- **API Validation**: Frontend checks are for UX only; backend MUST enforce all authorization
- **Role Context**: User role information should be available in authentication context/state

### Error Messages

When authorization fails, return appropriate error messages:

- **403 Forbidden**: "Super admin privileges required" / "Support agent privileges required" / "Provisioning specialist privileges required"
- **401 Unauthorized**: "Authentication required" (when user is not authenticated)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Internal staff can complete onboarding of a new organization and store from "Contract Signed" to "Fully Provisioned" (including organization member invitation) in under 30 minutes.
- **SC-002**: Zero errors occur in mapping physical IoT controllers to logical machine labels during provisioning (100% accuracy in hardware-to-software mapping).
- **SC-003**: System health dashboard displays connectivity status for all stores with updates visible within 30 seconds of a status change.
- **SC-004**: Support Agents can successfully troubleshoot operator-reported issues using Shadow View in 90% of cases without requiring operator screen sharing.
- **SC-005**: Super-Admins can update agent configuration for a store and have changes take effect for operators within 1 minute.
- **SC-006**: 95% of organization member invitations result in successful account creation and first login within 24 hours of invitation being sent.
- **SC-007**: System health alerts for offline stores are generated within 2 minutes of connectivity loss being detected.

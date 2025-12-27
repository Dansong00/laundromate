# Feature Specification: Super-User Admin Dashboard (Control Room)

**Feature Branch**: `001-super-admin-dashboard`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "PRD: Laundromaid Super-User Admin Dashboard (The \"Control Room\")"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organization and Store Onboarding (Priority: P1)

Internal staff need to create new customer organizations and their physical store locations through a guided onboarding wizard, then invite the store owner to access their dashboard.

**Why this priority**: Without this capability, new customers cannot be onboarded. This is the foundational workflow that enables all other operations. The system cannot provision new stores without this feature.

**Independent Test**: Can be fully tested by creating a new organization with one store and verifying the store owner invitation email is sent. Delivers value by enabling new customer onboarding.

**Acceptance Scenarios**:

1. **Given** a Super-Admin is logged into the Control Room, **When** they complete the onboarding wizard to create an organization named "Sunny Laundromat LLC" with address "123 Main St", **Then** the organization is created and stored in the system.
2. **Given** an organization exists, **When** a Super-Admin adds a new store location "Downtown Branch" with address "456 Oak Ave", **Then** the store is associated with the organization and displayed in the organization's store list.
3. **Given** a store has been created, **When** a Super-Admin invites a store owner by entering their email address "dan@example.com", **Then** an invitation email is sent and the user account is created with owner permissions for that store.
4. **Given** a store owner invitation has been sent, **When** the owner clicks the invitation link, **Then** they are prompted to set a password and granted access to their store dashboard.

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

- What happens when a store owner's email address is already in use by another user?
- How does the system handle duplicate MAC addresses or serial numbers during IoT provisioning?
- What happens when an organization has no stores created yet - can it exist?
- How does the system handle stores with no IoT controllers provisioned - do they appear in health monitoring?
- What happens when all agents are disabled for a store - what features remain accessible to operators?
- How does the system handle expired or invalid store owner invitations?
- What happens when an IoT controller is mapped to a machine that is later deleted?
- How does the system handle stores that have been deleted but still have active IoT controllers?
- What happens when a Support Agent tries to view as operator for a store they don't have permission to access?
- How does the system handle concurrent updates to agent configuration by multiple Super-Admins?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an onboarding wizard that guides internal staff through creating an organization with required details (name, address, contact information).
- **FR-002**: System MUST allow creation of multiple store locations under a single organization, each with its own address and identifier.
- **FR-003**: System MUST support sending email invitations to store owners with secure invitation links that expire after a configurable time period.
- **FR-004**: System MUST enforce role-based access control with three distinct roles: Super-Admin (full access), Support Agent (read-only financial data, can reset passwords), and Provisioning Specialist (machine mapping and store setup).
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
- **FR-015**: System MUST require store owner email addresses to be unique across the system.
- **FR-016**: System MUST allow Support Agents to reset user passwords for store owners and operators.
- **FR-017**: System MUST display machine mapping information (controller identifier, assigned label) in a searchable, sortable table format.
- **FR-018**: System MUST allow updating machine labels after initial provisioning without requiring controller re-provisioning.
- **FR-019**: System MUST display system health status in a high-density, data-rich interface optimized for internal staff use.
- **FR-020**: System MUST support filtering and searching stores by organization name, store name, status, or location in health monitoring views.

### Key Entities *(include if feature involves data)*

- **Organization**: Represents the parent company that owns one or more store locations. Attributes include name, billing address, contact information, and creation date. Relationships: has many Stores, has many Users (organization-level admins).

- **Store**: Represents a physical laundromat location. Attributes include name, street address, city, state, postal code, organization affiliation, status (active/inactive), and creation date. Relationships: belongs to one Organization, has many IoT Controllers, has many Users (store owners/operators), has Agent Configuration.

- **IoT Controller**: Represents a physical hardware device installed on a machine. Attributes include MAC address (unique identifier), serial number (optional unique identifier), store affiliation, assigned machine label, provisioned date, and connectivity status. Relationships: belongs to one Store, mapped to one Machine Label.

- **Machine Label**: Represents the logical name/label assigned to a physical machine in the operator's dashboard. Attributes include label text (e.g., "Washer #1"), store affiliation, and IoT controller association. Relationships: belongs to one Store, associated with one IoT Controller.

- **Agent Configuration**: Represents the subscription/feature access settings for a store. Attributes include store affiliation, enabled agents list, and last updated timestamp. Relationships: belongs to one Store, references multiple AI Agents.

- **AI Agent**: Represents an available intelligent agent feature (e.g., Maintenance Prophet, Pricing Strategist). Attributes include agent name, description, and availability status. Relationships: can be enabled/disabled per Store via Agent Configuration.

- **System Health Status**: Represents the current operational state of a store's IoT infrastructure. Attributes include store affiliation, connectivity status (online/offline), last heartbeat timestamp, alert count, and device status summary. Relationships: belongs to one Store.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Internal staff can complete onboarding of a new organization and store from "Contract Signed" to "Fully Provisioned" (including owner invitation) in under 30 minutes.
- **SC-002**: Zero errors occur in mapping physical IoT controllers to logical machine labels during provisioning (100% accuracy in hardware-to-software mapping).
- **SC-003**: System health dashboard displays connectivity status for all stores with updates visible within 30 seconds of a status change.
- **SC-004**: Support Agents can successfully troubleshoot operator-reported issues using Shadow View in 90% of cases without requiring operator screen sharing.
- **SC-005**: Super-Admins can update agent configuration for a store and have changes take effect for operators within 1 minute.
- **SC-006**: 95% of store owner invitations result in successful account creation and first login within 24 hours of invitation being sent.
- **SC-007**: System health alerts for offline stores are generated within 2 minutes of connectivity loss being detected.

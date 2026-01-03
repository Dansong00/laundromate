# Data Model: Super-User Admin Dashboard

**Feature**: Super-User Admin Dashboard (Control Room)
**Date**: 2025-12-27

## Overview

This document defines the data model for the Super-User Admin Dashboard feature. All entities extend the existing database schema and follow established patterns.

## Entities

### Organization

Represents the parent company that owns one or more store locations.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier
- `name` (String, Required): Company name (e.g., "Sunny Laundromat LLC")
- `billing_address` (String, Required): Street address for billing
- `city` (String, Required): City
- `state` (String, Required): State/Province
- `postal_code` (String, Required): Postal/ZIP code
- `country` (String, Required): Country code (ISO 3166-1 alpha-2)
- `contact_email` (String, Optional): Primary contact email
- `contact_phone` (String, Optional): Primary contact phone
- `status` (Enum: active, inactive, suspended, Required): Organization status
- `created_at` (DateTime, Required): Creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

**Relationships**:
- Has many `Store` (one-to-many)
- Has many `User` via UserOrganization (organization-level members with roles, optional)

**Validation Rules**:
- `name` must be unique across active organizations
- `contact_email` must be valid email format if provided
- `contact_phone` must be valid phone format if provided
- `status` defaults to "active" on creation

**State Transitions**:
- `active` → `inactive`: Organization deactivated
- `active` → `suspended`: Organization suspended (temporary)
- `inactive` → `active`: Organization reactivated
- `suspended` → `active`: Suspension lifted

### UserOrganization

Represents the many-to-many relationship between Users and Organizations for organization-level access.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier
- `user_id` (UUID, Foreign Key → User, Required): Associated user
- `organization_id` (UUID, Foreign Key → Organization, Required): Associated organization
- `role` (Enum: owner, employee, admin, Required): User's role within the organization
- `created_at` (DateTime, Required): Creation timestamp

**Relationships**:
- Belongs to one `User` (many-to-one)
- Belongs to one `Organization` (many-to-one)

**Validation Rules**:
- `user_id` and `organization_id` combination must be unique
- `role` defaults to "owner" on creation

**Permission Model**:
- `owner`: Full access to all stores in the organization
- `employee`: Access determined by organization admin (store assignments managed separately)
- `admin`: Administrative access within organization (store assignments managed separately)

### Store

Represents a physical laundromat location.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier
- `organization_id` (UUID, Foreign Key → Organization, Required): Parent organization
- `name` (String, Required): Store name (e.g., "Downtown Branch")
- `street_address` (String, Required): Street address
- `city` (String, Required): City
- `state` (String, Required): State/Province
- `postal_code` (String, Required): Postal/ZIP code
- `country` (String, Required): Country code (ISO 3166-1 alpha-2)
- `status` (Enum: active, inactive, Required): Store status
- `created_at` (DateTime, Required): Creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

**Relationships**:
- Belongs to one `Organization` (many-to-one)
- Has many `IoT Controller` (one-to-many)
- Has many `User` via UserStore (store owners/operators, for store-specific access, optional)
- Has one `Agent Configuration` (one-to-one)

**Note**: Organization-level users (via UserOrganization) have automatic access to all stores in their organization.

**Validation Rules**:
- `name` must be unique within the organization
- `organization_id` must reference an existing organization
- `status` defaults to "active" on creation

**State Transitions**:
- `active` → `inactive`: Store deactivated
- `inactive` → `active`: Store reactivated

### IoT Controller

Represents a physical hardware device installed on a machine.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier
- `store_id` (UUID, Foreign Key → Store, Required): Associated store
- `mac_address` (String, Required, Unique per store): MAC address (format: AA:BB:CC:DD:EE:FF)
- `serial_number` (String, Optional, Unique per store): Serial number (if available)
- `machine_label` (String, Required): Logical label (e.g., "Washer #1", "Dryer #3")
- `device_type` (Enum: washer, dryer, other, Required): Type of machine
- `connectivity_status` (Enum: online, offline, unknown, Required): Current connectivity status
- `last_heartbeat` (DateTime, Optional): Last heartbeat timestamp
- `provisioned_at` (DateTime, Required): Provisioning timestamp
- `created_at` (DateTime, Required): Creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

**Relationships**:
- Belongs to one `Store` (many-to-one)

**Validation Rules**:
- `mac_address` must be unique within the store (can be duplicated across stores)
- `serial_number` must be unique within the store if provided (can be duplicated across stores)
- `mac_address` must match format: `^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$`
- `machine_label` must be non-empty and max 100 characters
- `connectivity_status` defaults to "unknown" on creation

**State Transitions**:
- `unknown` → `online`: Controller connected and responding
- `online` → `offline`: Connectivity lost
- `offline` → `online`: Connectivity restored
- `online` → `unknown`: Heartbeat timeout (after 5 minutes)

### Agent Configuration

Represents the subscription/feature access settings for a store.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier
- `store_id` (UUID, Foreign Key → Store, Required, Unique): Associated store (one-to-one)
- `enabled_agents` (JSON Array of Strings, Required): List of enabled AI agent identifiers
- `last_updated_at` (DateTime, Required): Last configuration update timestamp
- `last_updated_by` (UUID, Foreign Key → User, Required): User who made last update
- `created_at` (DateTime, Required): Creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

**Relationships**:
- Belongs to one `Store` (one-to-one)
- References many `AI Agent` (via enabled_agents array)
- Updated by `User` (many-to-one)

**Validation Rules**:
- `store_id` must reference an existing store
- `enabled_agents` must contain valid AI agent identifiers
- `enabled_agents` defaults to empty array `[]` on creation
- `last_updated_by` must reference a Super-Admin user

**State Transitions**:
- Agents can be added/removed from `enabled_agents` array
- Changes take effect immediately (no approval workflow)

### AI Agent

Represents an available intelligent agent feature.

**Attributes**:
- `id` (String, Primary Key): Agent identifier (e.g., "maintenance_prophet", "pricing_strategist")
- `name` (String, Required): Display name (e.g., "Maintenance Prophet")
- `description` (String, Optional): Agent description
- `category` (Enum: maintenance, pricing, scheduling, analytics, other, Required): Agent category
- `is_available` (Boolean, Required): Whether agent is available for activation
- `created_at` (DateTime, Required): Creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

**Relationships**:
- Referenced by many `Agent Configuration` (via enabled_agents array)

**Validation Rules**:
- `id` must be unique and follow snake_case format
- `name` must be non-empty and max 100 characters
- `is_available` defaults to `true` on creation

**State Transitions**:
- `is_available: true` → `false`: Agent deprecated/disabled globally
- `is_available: false` → `true`: Agent re-enabled globally

### System Health Status

Represents the current operational state of a store's IoT infrastructure (derived/calculated entity, not stored directly).

**Attributes** (calculated from IoT Controllers):
- `store_id` (UUID): Associated store
- `connectivity_status` (Enum: online, offline, partial, unknown): Overall connectivity status
- `online_controllers` (Integer): Count of online controllers
- `offline_controllers` (Integer): Count of offline controllers
- `total_controllers` (Integer): Total controller count
- `last_heartbeat` (DateTime): Most recent heartbeat from any controller
- `alert_count` (Integer): Number of active alerts
- `critical_alerts` (Integer): Number of critical alerts (offline > 5 minutes)

**Relationships**:
- Derived from `Store` and `IoT Controller` entities

**Calculation Rules**:
- `connectivity_status` = "online" if all controllers are online
- `connectivity_status` = "offline" if all controllers are offline
- `connectivity_status` = "partial" if some controllers are online and some offline
- `connectivity_status` = "unknown" if no controllers exist
- `alert_count` = count of controllers offline > 2 minutes
- `critical_alerts` = count of controllers offline > 5 minutes

## Database Schema Changes

### New Tables
1. `organizations` - Organization entity
2. `user_organizations` - UserOrganization entity (many-to-many relationship)
3. `stores` - Store entity
4. `iot_controllers` - IoT Controller entity
5. `agent_configurations` - Agent Configuration entity
6. `ai_agents` - AI Agent entity (reference data, seeded on migration)

### New Indexes
- `organizations.name` (unique, partial: status = 'active')
- `user_organizations.user_id` (foreign key index)
- `user_organizations.organization_id` (foreign key index)
- `user_organizations.user_id, organization_id` (unique composite index)
- `stores.organization_id` (foreign key index)
- `stores.name` (unique within organization)
- `iot_controllers.store_id` (foreign key index)
- `iot_controllers.mac_address` (unique within store)
- `iot_controllers.serial_number` (unique within store, partial: serial_number IS NOT NULL)
- `agent_configurations.store_id` (unique foreign key index)

### Foreign Key Constraints
- `user_organizations.user_id` → `users.id` (CASCADE on delete)
- `user_organizations.organization_id` → `organizations.id` (CASCADE on delete)
- `stores.organization_id` → `organizations.id` (CASCADE on delete)
- `iot_controllers.store_id` → `stores.id` (CASCADE on delete)
- `agent_configurations.store_id` → `stores.id` (CASCADE on delete)
- `agent_configurations.last_updated_by` → `users.id` (RESTRICT on delete)

## Data Migration Strategy

1. Create new tables via Alembic migration
2. Seed `ai_agents` table with initial agent definitions:
   - `maintenance_prophet` - Maintenance Prophet
   - `pricing_strategist` - Pricing Strategist
   - (Additional agents added as needed)
3. No data migration required for existing entities (new feature)

## Validation Summary

- All required fields are non-nullable
- Unique constraints prevent duplicate organizations, stores, and IoT controllers
- Foreign key constraints maintain referential integrity
- Enum types restrict values to valid states
- Timestamps automatically managed by database

"""add super admin dashboard tables

Revision ID: a1b2c3d4e5f6
Revises: 38b74cbbbf7a
Create Date: 2025-12-27 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "38b74cbbbf7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add role columns to users table
    op.add_column(
        "users",
        sa.Column(
            "is_support_agent", sa.Boolean(), nullable=False, server_default="false"
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_provisioning_specialist",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    op.create_index(
        op.f("ix_users_is_support_agent"), "users", ["is_support_agent"], unique=False
    )
    op.create_index(
        op.f("ix_users_is_provisioning_specialist"),
        "users",
        ["is_provisioning_specialist"],
        unique=False,
    )

    # Create organizations table
    op.create_table(
        "organizations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("billing_address", sa.String(500), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("postal_code", sa.String(20), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(50), nullable=True),
        sa.Column(
            "status",
            sa.Enum("active", "inactive", "suspended", name="organizationstatus"),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organizations_name"), "organizations", ["name"])
    op.create_index(
        "ix_organizations_name_active",
        "organizations",
        ["name"],
        unique=True,
        postgresql_where=sa.text("status = 'active'"),
    )

    # Create stores table
    op.create_table(
        "stores",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "organization_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("street_address", sa.String(500), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("postal_code", sa.String(20), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column(
            "status",
            sa.Enum("active", "inactive", name="storestatus"),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(op.f("ix_stores_organization_id"), "stores", ["organization_id"])
    op.create_unique_constraint(
        "uq_store_org_name", "stores", ["organization_id", "name"]
    )

    # Create iot_controllers table
    op.create_table(
        "iot_controllers",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "store_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column("mac_address", sa.String(17), nullable=False),
        sa.Column("serial_number", sa.String(100), nullable=True),
        sa.Column("machine_label", sa.String(100), nullable=False),
        sa.Column(
            "device_type",
            sa.Enum("washer", "dryer", "other", name="devicetype"),
            nullable=False,
        ),
        sa.Column(
            "connectivity_status",
            sa.Enum("online", "offline", "unknown", name="connectivitystatus"),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "provisioned_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        op.f("ix_iot_controllers_store_id"), "iot_controllers", ["store_id"]
    )
    op.create_unique_constraint(
        "uq_iot_store_mac", "iot_controllers", ["store_id", "mac_address"]
    )
    op.create_index(
        "ix_iot_store_serial",
        "iot_controllers",
        ["store_id", "serial_number"],
        unique=True,
        postgresql_where=sa.text("serial_number IS NOT NULL"),
    )

    # Create ai_agents table
    op.create_table(
        "ai_agents",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column(
            "category",
            sa.Enum(
                "maintenance",
                "pricing",
                "scheduling",
                "analytics",
                "other",
                name="agentcategory",
            ),
            nullable=False,
        ),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create agent_configurations table
    op.create_table(
        "agent_configurations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "store_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "enabled_agents",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "last_updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_updated_by",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["last_updated_by"],
            ["users.id"],
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("store_id"),
    )
    op.create_index(
        op.f("ix_agent_configurations_store_id"),
        "agent_configurations",
        ["store_id"],
        unique=True,
    )

    # Create invitations table
    op.create_table(
        "invitations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column(
            "store_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "invited_by",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "pending", "accepted", "expired", "revoked", name="invitationstatus"
            ),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["invited_by"],
            ["users.id"],
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("token"),
    )
    op.create_index(op.f("ix_invitations_token"), "invitations", ["token"], unique=True)
    op.create_index(op.f("ix_invitations_email"), "invitations", ["email"])
    op.create_index(op.f("ix_invitations_store_id"), "invitations", ["store_id"])
    op.create_index(op.f("ix_invitations_status"), "invitations", ["status"])
    op.create_index(op.f("ix_invitations_expires_at"), "invitations", ["expires_at"])

    # Create user_stores table
    op.create_table(
        "user_stores",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "store_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum("owner", "operator", name="userstorerole"),
            nullable=False,
            server_default="owner",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "store_id", name="ix_user_stores_user_store"),
    )
    op.create_index(op.f("ix_user_stores_user_id"), "user_stores", ["user_id"])
    op.create_index(op.f("ix_user_stores_store_id"), "user_stores", ["store_id"])

    # Seed ai_agents table with initial agents
    op.execute(
        """
        INSERT INTO ai_agents (id, name, description, category, is_available,
        created_at, updated_at)
        VALUES
            ('maintenance_prophet', 'Maintenance Prophet', 'Predicts maintenance
            needs and schedules service', 'maintenance', true, now(), now()),
            ('pricing_strategist', 'Pricing Strategist', 'Optimizes pricing based
            on demand and market conditions', 'pricing', true, now(), now())
        ON CONFLICT (id) DO NOTHING;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order
    op.drop_table("user_stores")
    op.drop_table("invitations")
    op.drop_table("agent_configurations")
    op.drop_table("ai_agents")
    op.drop_table("iot_controllers")
    op.drop_table("stores")
    op.drop_table("organizations")

    # Drop user role columns
    op.drop_index(op.f("ix_users_is_provisioning_specialist"), table_name="users")
    op.drop_index(op.f("ix_users_is_support_agent"), table_name="users")
    op.drop_column("users", "is_provisioning_specialist")
    op.drop_column("users", "is_support_agent")

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS organizationstatus")
    op.execute("DROP TYPE IF EXISTS storestatus")
    op.execute("DROP TYPE IF EXISTS devicetype")
    op.execute("DROP TYPE IF EXISTS connectivitystatus")
    op.execute("DROP TYPE IF EXISTS agentcategory")
    op.execute("DROP TYPE IF EXISTS invitationstatus")
    op.execute("DROP TYPE IF EXISTS userstorerole")

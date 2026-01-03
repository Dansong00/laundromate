"""refactor invitations to organization level

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2024-01-15 12:00:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_organizations table
    op.create_table(
        "user_organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "role",
            sa.Enum("OWNER", "EMPLOYEE", "ADMIN", name="userorganizationrole"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_organizations_organization_id"),
        "user_organizations",
        ["organization_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_organizations_user_id"),
        "user_organizations",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_user_organizations_user_org",
        "user_organizations",
        ["user_id", "organization_id"],
        unique=True,
    )

    # Add organization_role enum to invitations table
    op.execute(
        "CREATE TYPE userorganizationrole AS ENUM ('OWNER', 'EMPLOYEE', 'ADMIN')"
    )

    # Add new columns to invitations table (non-nullable since no existing data)
    op.add_column(
        "invitations",
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        "invitations",
        sa.Column(
            "organization_role",
            postgresql.ENUM("OWNER", "EMPLOYEE", "ADMIN", name="userorganizationrole"),
            nullable=False,
            server_default="OWNER",
        ),
    )

    # Add foreign key constraint for organization_id
    op.create_foreign_key(
        "invitations_organization_id_fkey",
        "invitations",
        "organizations",
        ["organization_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Create index for organization_id
    op.create_index(
        op.f("ix_invitations_organization_id"),
        "invitations",
        ["organization_id"],
        unique=False,
    )

    # Drop old store_id column and foreign key
    op.drop_constraint("invitations_store_id_fkey", "invitations", type_="foreignkey")
    op.drop_index(op.f("ix_invitations_store_id"), table_name="invitations")
    op.drop_column("invitations", "store_id")


def downgrade() -> None:
    # Add back store_id column (nullable since no existing data to migrate back)
    op.add_column(
        "invitations",
        sa.Column("store_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # Add foreign key and index for store_id
    op.create_foreign_key(
        "invitations_store_id_fkey",
        "invitations",
        "stores",
        ["store_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        op.f("ix_invitations_store_id"),
        "invitations",
        ["store_id"],
        unique=False,
    )

    # Drop organization_id and organization_role columns
    op.drop_constraint(
        "invitations_organization_id_fkey", "invitations", type_="foreignkey"
    )
    op.drop_index(op.f("ix_invitations_organization_id"), table_name="invitations")
    op.drop_column("invitations", "organization_id")
    op.drop_column("invitations", "organization_role")

    # Drop user_organizations table
    op.drop_index("ix_user_organizations_user_org", table_name="user_organizations")
    op.drop_index(
        op.f("ix_user_organizations_user_id"), table_name="user_organizations"
    )
    op.drop_index(
        op.f("ix_user_organizations_organization_id"), table_name="user_organizations"
    )
    op.drop_table("user_organizations")

    # Drop enum type (only if not used elsewhere)
    op.execute("DROP TYPE IF EXISTS userorganizationrole")

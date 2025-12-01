"""add super admin to users

Revision ID: 38b74cbbbf7a
Revises: 9039b0cba195
Create Date: 2025-01-15 15:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "38b74cbbbf7a"
down_revision: Union[str, Sequence[str], None] = "9039b0cba195"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add is_super_admin column to users table
    op.add_column(
        "users",
        sa.Column(
            "is_super_admin", sa.Boolean(), nullable=False, server_default="false"
        ),
    )
    # Create index on is_super_admin for efficient queries
    op.create_index(
        op.f("ix_users_is_super_admin"), "users", ["is_super_admin"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index
    op.drop_index(op.f("ix_users_is_super_admin"), table_name="users")
    # Drop column
    op.drop_column("users", "is_super_admin")

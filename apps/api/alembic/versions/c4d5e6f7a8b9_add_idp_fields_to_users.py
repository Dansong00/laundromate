"""add idp fields to users

Revision ID: c4d5e6f7a8b9
Revises: b2c3d4e5f6a7
Create Date: 2025-02-20 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "c4d5e6f7a8b9"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("auth_provider", sa.String(32), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("auth_provider_sub", sa.String(255), nullable=True),
    )
    op.create_index(
        op.f("ix_users_auth_provider"),
        "users",
        ["auth_provider"],
        unique=False,
    )
    op.create_index(
        op.f("ix_users_auth_provider_sub"),
        "users",
        ["auth_provider_sub"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_users_auth_provider_sub"), table_name="users")
    op.drop_index(op.f("ix_users_auth_provider"), table_name="users")
    op.drop_column("users", "auth_provider_sub")
    op.drop_column("users", "auth_provider")

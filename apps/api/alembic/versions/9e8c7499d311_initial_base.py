"""initial base

Revision ID: 9e8c7499d311
Revises:
Create Date: 2025-08-28 19:16:54.672883

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "9e8c7499d311"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""

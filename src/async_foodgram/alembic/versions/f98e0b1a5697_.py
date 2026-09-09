"""empty message

Revision ID: f98e0b1a5697
Revises: c64a9d7b5cba
Create Date: 2026-08-30 23:43:39.647595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f98e0b1a5697'
down_revision: Union[str, Sequence[str], None] = 'c64a9d7b5cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

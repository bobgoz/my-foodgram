"""empty message

Revision ID: c49bd32ed468
Revises: f98e0b1a5697
Create Date: 2026-08-30 23:56:41.333060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c49bd32ed468'
down_revision: Union[str, Sequence[str], None] = 'f98e0b1a5697'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

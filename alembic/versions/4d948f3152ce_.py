"""empty message

Revision ID: 4d948f3152ce
Revises: 2af7c02b56d5
Create Date: 2026-07-18 13:27:29.685565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d948f3152ce'
down_revision: Union[str, Sequence[str], None] = '2af7c02b56d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

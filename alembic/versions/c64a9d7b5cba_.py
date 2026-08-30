"""empty message

Revision ID: c64a9d7b5cba
Revises: 3988a209449b
Create Date: 2026-08-30 23:43:37.084946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c64a9d7b5cba'
down_revision: Union[str, Sequence[str], None] = '3988a209449b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

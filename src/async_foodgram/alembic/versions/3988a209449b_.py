"""empty message

Revision ID: 3988a209449b
Revises: 2ef2e424df38
Create Date: 2026-08-30 23:43:00.215422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3988a209449b'
down_revision: Union[str, Sequence[str], None] = '2ef2e424df38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

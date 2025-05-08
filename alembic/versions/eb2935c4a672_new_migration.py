"""New migration

Revision ID: eb2935c4a672
Revises: 6bf2f14a6e03
Create Date: 2025-05-03 11:35:30.932563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb2935c4a672'
down_revision: Union[str, None] = '6bf2f14a6e03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

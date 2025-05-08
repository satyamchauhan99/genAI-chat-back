"""init

Revision ID: 9500cb328d08
Revises: 137a9d2082d9
Create Date: 2025-05-03 11:28:39.392160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9500cb328d08'
down_revision: Union[str, None] = '137a9d2082d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

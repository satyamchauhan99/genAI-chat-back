"""Update Table

Revision ID: eac291427c77
Revises: fa38607b86ac
Create Date: 2025-05-03 18:45:00.538445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac291427c77'
down_revision: Union[str, None] = 'fa38607b86ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: Add current_status column to documents."""
    op.add_column(
        'documents',
        sa.Column('current_status', sa.Integer(), nullable=False, server_default='1')
    )
    # Remove server_default after column is created to avoid issues on insert
    op.alter_column('documents', 'current_status', server_default=None)


def downgrade() -> None:
    """Downgrade schema: Remove current_status column from documents."""
    op.drop_column('documents', 'current_status')
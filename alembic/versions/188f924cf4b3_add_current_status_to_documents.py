"""Add current_status to documents

Revision ID: 188f924cf4b3
Revises: eac291427c77
Create Date: 2025-05-03 18:49:40.376735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '188f924cf4b3'
down_revision: Union[str, None] = 'eac291427c77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the column with a default value so it works on existing rows
    op.add_column('documents',
        sa.Column('current_status', sa.Integer(), nullable=False, server_default='1')
    )
    # Drop default afterward to avoid locking it permanently
    op.alter_column('documents', 'current_status', server_default=None)


def downgrade():
    op.drop_column('documents', 'current_status')

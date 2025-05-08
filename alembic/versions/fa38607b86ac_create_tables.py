"""Create tables

Revision ID: fa38607b86ac
Revises: eb2935c4a672
Create Date: 2025-05-03 11:41:34.179121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa38607b86ac'
down_revision: Union[str, None] = 'eb2935c4a672'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id")),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('documents')
    op.drop_table('users')

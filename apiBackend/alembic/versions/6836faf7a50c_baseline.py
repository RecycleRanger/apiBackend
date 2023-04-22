"""baseline

Revision ID: 6836faf7a50c
Revises: 
Create Date: 2023-04-22 20:15:22.100537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6836faf7a50c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'bug',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bug_tracker', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('bug')

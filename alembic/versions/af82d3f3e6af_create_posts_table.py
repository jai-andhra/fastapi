"""create posts table

Revision ID: af82d3f3e6af
Revises: 6df54b6a9ec4
Create Date: 2021-11-16 21:45:19.658271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af82d3f3e6af'
down_revision = '6df54b6a9ec4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

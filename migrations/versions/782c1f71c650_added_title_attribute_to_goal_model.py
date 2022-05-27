"""added title attribute to Goal model

Revision ID: 782c1f71c650
Revises: 54759d7b673c
Create Date: 2022-05-27 07:37:47.163325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782c1f71c650'
down_revision = '54759d7b673c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###

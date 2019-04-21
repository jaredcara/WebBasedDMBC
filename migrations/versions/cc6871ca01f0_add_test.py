"""add test

Revision ID: cc6871ca01f0
Revises: 247925620e24
Create Date: 2019-04-18 14:22:55.769318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc6871ca01f0'
down_revision = '247925620e24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('testing', sa.PickleType(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'testing')
    # ### end Alembic commands ###

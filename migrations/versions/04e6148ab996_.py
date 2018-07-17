"""empty message

Revision ID: 04e6148ab996
Revises: 52276db0dc9a
Create Date: 2018-06-18 16:31:09.554080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e6148ab996'
down_revision = '52276db0dc9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Request', sa.Column('description', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Request', 'description')
    # ### end Alembic commands ###
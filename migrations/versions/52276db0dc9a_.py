"""empty message

Revision ID: 52276db0dc9a
Revises: 54e149d67b54
Create Date: 2018-06-18 15:22:28.195570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52276db0dc9a'
down_revision = '54e149d67b54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Request', 'status',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Request', 'status',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###

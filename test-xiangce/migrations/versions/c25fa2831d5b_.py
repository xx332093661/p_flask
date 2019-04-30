"""empty message

Revision ID: c25fa2831d5b
Revises: 3d43e153bf5e
Create Date: 2017-10-10 15:10:53.775000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c25fa2831d5b'
down_revision = '3d43e153bf5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', mysql.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###
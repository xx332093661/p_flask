"""empty message

Revision ID: b17ee979ed92
Revises: fd61e76d7fe8
Create Date: 2017-10-19 10:45:37.490000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b17ee979ed92'
down_revision = 'fd61e76d7fe8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('cover', sa.String(length=64), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('tag', sa.String(length=64), nullable=True),
    sa.Column('no_public', sa.Boolean(), nullable=True),
    sa.Column('no_comment', sa.Boolean(), nullable=True),
    sa.Column('asc_order', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_albums_timestamp'), 'albums', ['timestamp'], unique=False)
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.add_column(u'photos', sa.Column('album_id', sa.Integer(), nullable=True))
    op.add_column(u'photos', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'photos', 'albums', ['album_id'], ['id'])
    op.create_foreign_key(None, 'photos', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photos', type_='foreignkey')
    op.drop_constraint(None, 'photos', type_='foreignkey')
    op.drop_column(u'photos', 'author_id')
    op.drop_column(u'photos', 'album_id')
    op.drop_table('follows')
    op.drop_index(op.f('ix_albums_timestamp'), table_name='albums')
    op.drop_table('albums')
    # ### end Alembic commands ###

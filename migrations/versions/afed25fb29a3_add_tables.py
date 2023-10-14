"""Add tables

Revision ID: afed25fb29a3
Revises: 3c97ef3d648f
Create Date: 2023-10-14 08:10:09.868327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afed25fb29a3'
down_revision: Union[str, None] = '3c97ef3d648f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posttypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('active_project', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('postimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('like', sa.Boolean(), nullable=True),
    sa.Column('dislike', sa.Boolean(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('style', sa.String(), nullable=False),
    sa.Column('seed', sa.BigInteger(), nullable=True),
    sa.Column('prompt', sa.Text(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('themes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('post_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_type_id'], ['posttypes.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('like', sa.Boolean(), nullable=True),
    sa.Column('dislike', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('theme_id', sa.Integer(), nullable=True),
    sa.Column('theme_text', sa.Text(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['theme_id'], ['themes.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('themes')
    op.drop_table('projects')
    op.drop_table('postimage')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('posttypes')
    # ### end Alembic commands ###
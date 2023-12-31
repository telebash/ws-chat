"""fix

Revision ID: 36e795585ef3
Revises: 28c3b950e855
Create Date: 2023-11-07 21:53:51.029481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36e795585ef3'
down_revision: Union[str, None] = '28c3b950e855'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('theme')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('theme',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_type_id'], ['posttype.id'], name='theme_post_type_id_fkey', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name='theme_project_id_fkey', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='theme_pkey')
    )
    # ### end Alembic commands ###

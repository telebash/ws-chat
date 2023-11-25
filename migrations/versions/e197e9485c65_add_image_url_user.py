"""add image_url user

Revision ID: e197e9485c65
Revises: 0af8845acbc4
Create Date: 2023-11-19 05:38:56.035892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e197e9485c65'
down_revision: Union[str, None] = '0af8845acbc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_url')
    # ### end Alembic commands ###

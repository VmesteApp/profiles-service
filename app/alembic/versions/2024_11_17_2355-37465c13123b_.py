"""empty message

Revision ID: 37465c13123b
Revises: 134bc8e3bf17
Create Date: 2024-11-17 23:55:37.585771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37465c13123b'
down_revision: Union[str, None] = '134bc8e3bf17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('notification', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'updated_at')
    op.drop_column('notification', 'created_at')
    # ### end Alembic commands ###

"""added column to order-product

Revision ID: 67f9b802a825
Revises: edbd5c8e34c4
Create Date: 2024-09-24 14:22:13.411358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67f9b802a825'
down_revision: Union[str, None] = 'edbd5c8e34c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_product_association', sa.Column('count', sa.Integer(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_product_association', 'count')
    # ### end Alembic commands ###
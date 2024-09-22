"""Create posts table

Revision ID: 1a0396ef297d
Revises: e09178be5a30
Create Date: 2024-09-22 21:40:58.478058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1a0396ef297d'
down_revision: Union[str, None] = 'e09178be5a30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('body', sa.Text(), server_default='', nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
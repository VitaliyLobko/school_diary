"""contacts fix

Revision ID: ff1b6d03d33f
Revises: 72aa6de6989c
Create Date: 2024-12-02 19:52:32.275056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff1b6d03d33f'
down_revision: Union[str, None] = '72aa6de6989c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'person_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('person_type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

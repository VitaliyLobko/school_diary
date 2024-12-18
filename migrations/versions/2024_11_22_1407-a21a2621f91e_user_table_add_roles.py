"""user table add roles

Revision ID: a21a2621f91e
Revises: 1854938cdcad
Create Date: 2024-11-22 14:07:30.121540

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a21a2621f91e"
down_revision: Union[str, None] = "1854938cdcad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE role AS ENUM ('admin', 'moderator', 'user')")
    op.add_column(
        "users",
        sa.Column(
            "roles",
            sa.Enum("admin", "moderator", "user", name="role"),
            nullable=True,
            default="user",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "roles")
    op.execute("DROP TYPE role)")
    # ### end Alembic commands ###

"""V_03__add_is_active_in_auth_from_user

Revision ID: dcdd91b1494a
Revises: 1ef016608af4
Create Date: 2023-08-23 14:50:59.108012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dcdd91b1494a"
down_revision: Union[str, None] = "1ef016608af4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("auths", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_column("auths", "is_active")
    # ### end Alembic commands ###

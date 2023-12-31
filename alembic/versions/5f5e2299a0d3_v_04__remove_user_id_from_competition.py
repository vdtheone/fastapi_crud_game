"""V_04__remove_user_id_from_competition

Revision ID: 5f5e2299a0d3
Revises: dcdd91b1494a
Create Date: 2023-08-24 10:17:23.842146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f5e2299a0d3"
down_revision: Union[str, None] = "dcdd91b1494a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("competitions_user_id_fkey", "competitions", type_="foreignkey")
    op.drop_column("competitions", "user_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "competitions",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "competitions_user_id_fkey", "competitions", "users", ["user_id"], ["id"]
    )
    # ### end Alembic commands ###

"""V_02__update_auth_add_foreign_key

Revision ID: 1ef016608af4
Revises: bba4925186ac
Create Date: 2023-08-23 12:26:55.285467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ef016608af4'
down_revision: Union[str, None] = 'bba4925186ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auths', 'age')
    op.drop_column('auths', 'gender')
    op.drop_column('auths', 'date_of_birth')
    op.drop_column('auths', 'is_active')
    op.drop_column('auths', 'name')
    op.add_column('users', sa.Column('auth_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(), nullable=True))
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'users', 'auths', ['auth_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'date_of_birth')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'auth_id')
    op.add_column('auths', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('auths', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('auths', sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('auths', sa.Column('gender', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('auths', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

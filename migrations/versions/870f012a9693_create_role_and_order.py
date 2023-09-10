"""Create role and order

Revision ID: 870f012a9693
Revises: 2677a52c8d6c
Create Date: 2023-09-10 22:54:09.360539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '870f012a9693'
down_revision: Union[str, None] = '2677a52c8d6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('date_of_purchase', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('Pending', 'Shipped', 'Delivered', 'Canceled', 'Refunded', name='orderstatus', create_constraint=True), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('item', 'added_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('item', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('item', 'rating',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('item', 'amount',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('item', 'type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('role', sa.Column('permissions', sa.String(), nullable=False))
    op.drop_column('role', 'permission')
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('username', sa.String(), nullable=False))
    op.add_column('user', sa.Column('registered_at', sa.TIMESTAMP(), nullable=False))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'registered_at')
    op.drop_column('user', 'username')
    op.drop_column('user', 'role_id')
    op.add_column('role', sa.Column('permission', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('role', 'permissions')
    op.alter_column('item', 'type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('item', 'amount',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('item', 'rating',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('item', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('item', 'added_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_table('order')
    # ### end Alembic commands ###

"""initial revision

Revision ID: 4502a236b57e
Revises: 
Create Date: 2023-09-22 18:13:30.512134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4502a236b57e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TYPE IF EXISTS orderstatus")
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('size', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('permission', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('date_of_purchase', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('Pending', 'Shipped', 'Delivered', 'Canceled', 'Refunded', name='orderstatus', create_constraint=True), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('item')
    # ### end Alembic commands ###

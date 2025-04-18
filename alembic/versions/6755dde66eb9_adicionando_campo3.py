"""Adicionando campo3

Revision ID: 6755dde66eb9
Revises: 170d7d719b14
Create Date: 2025-03-12 17:05:29.901423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6755dde66eb9'
down_revision: Union[str, None] = '170d7d719b14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_authorization_number_id', table_name='authorization_number')
    op.drop_table('authorization_number')
    op.drop_index('ix_spents_id', table_name='spents')
    op.drop_table('spents')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spents',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('recurring', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('installment_debt', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('purchase_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='spents_pkey')
    )
    op.create_index('ix_spents_id', 'spents', ['id'], unique=False)
    op.create_table('authorization_number',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('number', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='authorization_number_pkey')
    )
    op.create_index('ix_authorization_number_id', 'authorization_number', ['id'], unique=False)
    # ### end Alembic commands ###

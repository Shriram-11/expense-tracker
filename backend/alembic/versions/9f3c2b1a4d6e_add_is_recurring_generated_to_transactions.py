"""add_is_recurring_generated_to_transactions

Revision ID: 9f3c2b1a4d6e
Revises: 5992a2a1cda4
Create Date: 2026-02-15 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f3c2b1a4d6e'
down_revision: Union[str, None] = '5992a2a1cda4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'transactions',
        sa.Column(
            'is_recurring_generated',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )
    op.alter_column(
        'transactions',
        'is_recurring_generated',
        server_default=None
    )


def downgrade() -> None:
    op.drop_column('transactions', 'is_recurring_generated')

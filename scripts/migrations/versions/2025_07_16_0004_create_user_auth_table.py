"""create user_auth table

Revision ID: 3a6a1efaea06
Revises: 35d024da8e2e
Create Date: 2025-07-16 15:59:18.442807
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision: str = '3a6a1efaea06'
down_revision: Union[str, Sequence[str], None] = '35d024da8e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create user_auth table with constraints and index."""
    op.create_table(
        'user_auth',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('wrong_password_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('account_locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', name='fk_user_auth_user_id'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='SET NULL', name='fk_user_auth_created_by'),
        sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ondelete='SET NULL', name='fk_user_auth_updated_by'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username', name='uq_user_auth_username'),
    )
    op.create_index('ix_user_auth_deleted_at', 'user_auth', ['deleted_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema: Drop user_auth table and related constraints."""
    op.drop_constraint('fk_user_auth_updated_by', 'user_auth', type_='foreignkey')
    op.drop_constraint('fk_user_auth_created_by', 'user_auth', type_='foreignkey')
    op.drop_constraint('fk_user_auth_user_id', 'user_auth', type_='foreignkey')
    op.drop_constraint('uq_user_auth_username', 'user_auth', type_='unique')
    op.drop_index('ix_user_auth_deleted_at', table_name='user_auth')
    op.drop_table('user_auth')

"""create user_identity table

Revision ID: cc7dc0185304
Revises: 3a6a1efaea06
Create Date: 2025-07-16 19:47:33.144821
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = 'cc7dc0185304'
down_revision: Union[str, Sequence[str], None] = '3a6a1efaea06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create user_identity table with constraints and index."""
    op.create_table(
        'user_identity',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('EMAIL', 'MOBILE', 'OAUTH', name='identity_type'), nullable=False),
        sa.Column('value', sa.String(length=191), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column('is_primary', sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column('oauth_provider', sa.String(length=50), nullable=True),
        sa.Column('otp_code', sa.String(length=10), nullable=True),
        sa.Column('otp_generated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('wrong_otp_count', sa.Integer(), server_default="0", nullable=False),
        sa.Column('otp_locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', name='fk_user_identity_user_id'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='SET NULL', name='fk_user_identity_created_by'),
        sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ondelete='SET NULL', name='fk_user_identity_updated_by'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('type', 'value', 'oauth_provider', name='uq_user_identity_value'),
    )

    op.create_index('ix_user_identity_deleted_at', 'user_identity', ['deleted_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema: Drop user_identity table and its constraints/indexes."""
    op.drop_index('ix_user_identity_deleted_at', table_name='user_identity')
    op.drop_constraint('uq_user_identity_value', 'user_identity', type_='unique')
    op.drop_constraint('fk_user_identity_updated_by', 'user_identity', type_='foreignkey')
    op.drop_constraint('fk_user_identity_created_by', 'user_identity', type_='foreignkey')
    op.drop_constraint('fk_user_identity_user_id', 'user_identity', type_='foreignkey')
    op.drop_table('user_identity')

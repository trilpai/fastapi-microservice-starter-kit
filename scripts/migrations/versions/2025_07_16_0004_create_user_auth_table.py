"""🔐 Create `user_auth` table

Stores login credentials (username, password_hash) and authentication metadata
for users, including lockout tracking and last login timestamps.

Revision ID: 3a6a1efaea06
Revises: 35d024da8e2e
Create Date: 2025-07-16 15:59:18.442807
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = "3a6a1efaea06"
down_revision: Union[str, Sequence[str], None] = "35d024da8e2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Create `user_auth` table with constraints, audit fields, and indexes."""
    op.create_table(
        "user_auth",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key"),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="FK to `user.id`"),
        sa.Column("username", sa.String(length=100), nullable=True, comment="Optional unique username for login"),
        sa.Column("password_hash", sa.String(length=256), nullable=False, comment="Hashed password"),
        sa.Column("wrong_password_count", sa.Integer(), server_default="0", nullable=False, comment="Failed login attempts"),
        sa.Column("account_locked_until", sa.DateTime(timezone=True), nullable=True, comment="Time until account is locked"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True, comment="Timestamp of last successful login"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Last updated timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="User ID who created this record"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="User ID who last updated this record"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft delete timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_user_auth_id"),
        sa.UniqueConstraint("username", name="uq_user_auth_username"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE", name="fk_user_auth_user_id"),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="SET NULL", name="fk_user_auth_created_by"),
        sa.ForeignKeyConstraint(["updated_by"], ["user.id"], ondelete="SET NULL", name="fk_user_auth_updated_by"),
    )

    # Add supporting indexes
    op.create_index("ix_user_auth_deleted_at", "user_auth", ["deleted_at"], unique=False)
    op.create_index("ix_user_auth_user_id", "user_auth", ["user_id"], unique=False)


def downgrade() -> None:
    """🔽 Drop `user_auth` table, including indexes and constraints (SQLite-safe)."""

    # 🔻 Drop non-constraint indexes
    op.drop_index("ix_user_auth_user_id", table_name="user_auth")
    op.drop_index("ix_user_auth_deleted_at", table_name="user_auth")

    # 🔻 Drop constraints safely using batch mode (required for SQLite)
    with op.batch_alter_table("user_auth", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_auth_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_auth_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_auth_user_id", type_="foreignkey")
        batch_op.drop_constraint("uq_user_auth_username", type_="unique")
        batch_op.drop_constraint("pk_user_auth_id", type_="primary")

    # 🔻 Drop the table
    op.drop_table("user_auth")


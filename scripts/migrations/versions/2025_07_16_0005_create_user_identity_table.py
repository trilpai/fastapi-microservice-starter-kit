"""🆔 Create `user_identity` table

Stores multiple user identities such as emails, phone numbers, or OAuth UIDs
with verification, OTP, and primary designation capabilities.

Revision ID: cc7dc0185304
Revises: 3a6a1efaea06
Create Date: 2025-07-16 19:47:33.144821
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision: str = "cc7dc0185304"
down_revision: Union[str, Sequence[str], None] = "3a6a1efaea06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Create `user_identity` table with constraints, audit fields, and indexes."""
    op.create_table(
        "user_identity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key"),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="FK to user.id"),
        sa.Column("type", sa.Enum("EMAIL", "MOBILE", "OAUTH", name="identity_type"), nullable=False, comment="Identity type: email, mobile, or oauth"),
        sa.Column("value", sa.String(length=191), nullable=False, comment="Actual value: email, phone number, or OAuth UID"),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.text("0"), nullable=True, comment="Whether this identity has been verified"),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.text("0"), nullable=True, comment="Whether this is the user's primary identity"),
        sa.Column("oauth_provider", sa.String(length=50), nullable=True, comment="OAuth provider name (only if type=OAUTH)"),
        sa.Column("otp_code", sa.String(length=10), nullable=True, comment="Last OTP sent"),
        sa.Column("otp_generated_at", sa.DateTime(timezone=True), nullable=True, comment="Timestamp when OTP was generated"),
        sa.Column("wrong_otp_count", sa.Integer(), server_default="0", nullable=False, comment="Failed OTP entry attempts"),
        sa.Column("otp_locked_until", sa.DateTime(timezone=True), nullable=True, comment="OTP entry locked until this timestamp"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Last update timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="ID of user who created this entry"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="ID of user who last updated this entry"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft delete timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_user_identity_id"),
        sa.UniqueConstraint("type", "value", "oauth_provider", name="uq_user_identity_value"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE", name="fk_user_identity_user_id"),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="SET NULL", name="fk_user_identity_created_by"),
        sa.ForeignKeyConstraint(["updated_by"], ["user.id"], ondelete="SET NULL", name="fk_user_identity_updated_by"),
    )

    # Supporting indexes
    op.create_index("ix_user_identity_user_id", "user_identity", ["user_id"], unique=False)
    op.create_index("ix_user_identity_is_verified", "user_identity", ["is_verified"], unique=False)
    op.create_index("ix_user_identity_is_primary", "user_identity", ["is_primary"], unique=False)
    op.create_index("ix_user_identity_deleted_at", "user_identity", ["deleted_at"], unique=False)


def downgrade() -> None:
    """🔽 Drop `user_identity` table, including constraints and indexes, with SQLite-safe batch mode."""

    # 🔻 Drop indexes first
    op.drop_index("ix_user_identity_deleted_at", table_name="user_identity")
    op.drop_index("ix_user_identity_is_primary", table_name="user_identity")
    op.drop_index("ix_user_identity_is_verified", table_name="user_identity")
    op.drop_index("ix_user_identity_user_id", table_name="user_identity")

    # 🔻 Drop constraints using batch mode (required for SQLite compatibility)
    with op.batch_alter_table("user_identity", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_identity_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_identity_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_identity_user_id", type_="foreignkey")
        batch_op.drop_constraint("uq_user_identity_value", type_="unique")
        batch_op.drop_constraint("pk_user_identity_id", type_="primary")

    # 🔻 Finally, drop the table itself
    op.drop_table("user_identity")


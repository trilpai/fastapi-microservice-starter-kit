"""👤 Create `user` table

Defines system users and their core profile, role, and status attributes.

Revision ID: 1f89f8e4a935
Revises: 89362c213e43
Create Date: 2025-07-16 09:25:49.616752
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = "1f89f8e4a935"
down_revision: Union[str, Sequence[str], None] = "89362c213e43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Create the `user` table with audit fields, role FK, and indexes."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key"),
        sa.Column("first_name", sa.String(length=64), nullable=False, comment="User's first name"),
        sa.Column("last_name", sa.String(length=64), nullable=True, comment="User's last name"),
        sa.Column("job_title", sa.String(length=128), nullable=True, comment="Optional job title"),
        sa.Column("gender", sa.Enum("male", "female", "other", "prefer_not_to_say", name="gender"), nullable=True, comment="Optional gender enum"),
        sa.Column("dob", sa.Date(), nullable=True, comment="Date of birth"),
        sa.Column("profile_image_url", sa.String(length=512), nullable=True, comment="Profile image URL"),
        sa.Column("is_active", sa.Boolean(), server_default="1", nullable=False, comment="Flag indicating if user is active"),
        sa.Column("role_id", sa.Integer(), nullable=False, comment="Foreign key to role table"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Last updated timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="ID of creator"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="ID of last modifier"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft delete timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_user_id"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], ondelete="RESTRICT", name="fk_user_role_id"),
    )

    # Add supporting indexes
    op.create_index("ix_user_deleted_at", "user", ["deleted_at"], unique=False)
    op.create_index("ix_user_role_id", "user", ["role_id"], unique=False)
    op.create_index("ix_user_is_active", "user", ["is_active"], unique=False)


def downgrade() -> None:
    """🔽 Drop the `user` table, including constraints and indexes (SQLite-safe)."""

    # 🔻 Drop standalone indexes
    op.drop_index("ix_user_is_active", table_name="user")
    op.drop_index("ix_user_role_id", table_name="user")
    op.drop_index("ix_user_deleted_at", table_name="user")

    # 🔻 Drop constraints using batch mode (required for SQLite)
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_role_id", type_="foreignkey")
        batch_op.drop_constraint("pk_user_id", type_="primary")

    # 🔻 Drop the table
    op.drop_table("user")


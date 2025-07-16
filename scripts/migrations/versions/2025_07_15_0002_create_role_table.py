"""📜 Create `role` table

Defines the `role` table for user access roles (e.g., Admin, Viewer).
Includes metadata for soft-deletion, auditing, and a unique role name constraint.

Revision ID: dabace0963db
Revises: 39f025c30170
Create Date: 2025-07-15 22:24:06.361669
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = 'dabace0963db'
down_revision: Union[str, Sequence[str], None] = '39f025c30170'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Create `role` table with constraints and index."""
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key ID"),
        sa.Column("name", sa.String(length=64), nullable=False, comment="Unique name of the role (e.g., 'Admin')"),
        sa.Column("description", sa.String(length=256), nullable=True, comment="Optional human-readable role description"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Last update timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="User ID who created this record"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="User ID who last updated this record"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft delete marker timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_role_id"),
        sa.UniqueConstraint("name", name="uq_role_name"),
    )

    op.create_index(
        "ix_role_deleted_at",
        "role",
        ["deleted_at"],
        unique=False,
    )


def downgrade() -> None:
    """🔽 Drop the `role` table, including constraints and index (SQLite-compatible)."""

    # 🔻 Drop the soft-delete index
    op.drop_index("ix_role_deleted_at", table_name="role")

    # 🔻 Drop constraints using batch mode for SQLite support
    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.drop_constraint("uq_role_name", type_="unique")
        batch_op.drop_constraint("pk_role_id", type_="primary")

    # 🔻 Drop the table
    op.drop_table("role")


"""📜 Create `privilege` table

Defines the `privilege` table, which stores named access control units (e.g., "edit_users").
Includes support for soft-deletion, auditing, and a unique constraint on name.

Revision ID: 39f025c30170
Revises: None
Create Date: 2025-07-15 21:34:15.545181
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = '39f025c30170'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Apply schema changes — Create `privilege` table with constraints and index."""
    op.create_table(
        "privilege",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key ID"),
        sa.Column("name", sa.String(length=64), nullable=False, comment="Unique privilege name (e.g., 'view_dashboard')"),
        sa.Column("description", sa.String(length=256), nullable=True, comment="Optional description for the privilege"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), comment="Last update timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="ID of user who created this record"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="ID of user who last updated this record"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft-delete marker timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_privilege_id"),
        sa.UniqueConstraint("name", name="uq_privilege_name"),
    )

    # Soft-delete index for fast filtering
    op.create_index(
        "ix_privilege_deleted_at",
        "privilege",
        ["deleted_at"],
        unique=False,
    )


def downgrade() -> None:
    """🔽 Revert schema changes — Drop `privilege` table, constraints, and index (SQLite-safe)."""

    # 🔻 Drop the soft-delete index
    op.drop_index("ix_privilege_deleted_at", table_name="privilege")

    # 🔻 Drop constraints using batch mode for SQLite compatibility
    with op.batch_alter_table("privilege", schema=None) as batch_op:
        batch_op.drop_constraint("uq_privilege_name", type_="unique")
        batch_op.drop_constraint("pk_privilege_id", type_="primary")

    # 🔻 Drop the table
    op.drop_table("privilege")


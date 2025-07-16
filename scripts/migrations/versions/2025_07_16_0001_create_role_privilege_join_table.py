"""🔗 Create `role_privilege` join table

Defines many-to-many mapping between roles and privileges.
Ensures uniqueness of each pair and supports soft-deletion and auditing.

Revision ID: 89362c213e43
Revises: dabace0963db
Create Date: 2025-07-16 09:14:25.445741
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision: str = "89362c213e43"
down_revision: Union[str, Sequence[str], None] = "dabace0963db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """🆙 Create the `role_privilege` join table with constraints."""
    op.create_table(
        "role_privilege",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="Primary key"),
        sa.Column("role_id", sa.Integer(), nullable=False, comment="FK to role table"),
        sa.Column("privilege_id", sa.Integer(), nullable=False, comment="FK to privilege table"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment="Last update timestamp"),
        sa.Column("created_by", sa.Integer(), nullable=True, comment="User ID who created the record"),
        sa.Column("updated_by", sa.Integer(), nullable=True, comment="User ID who last updated the record"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Soft delete timestamp"),
        sa.PrimaryKeyConstraint("id", name="pk_role_privilege_id"),
        sa.UniqueConstraint("role_id", "privilege_id", name="uq_role_privilege"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], ondelete="CASCADE", name="fk_role_privilege_role_id"),
        sa.ForeignKeyConstraint(["privilege_id"], ["privilege.id"], ondelete="CASCADE", name="fk_role_privilege_privilege_id"),
    )

    op.create_index(
        "ix_role_privilege_deleted_at",
        "role_privilege",
        ["deleted_at"],
        unique=False,
    )


def downgrade() -> None:
    """🔽 Drop the `role_privilege` join table, including constraints and index (SQLite-safe)."""

    # 🔻 Drop the soft-delete index
    op.drop_index("ix_role_privilege_deleted_at", table_name="role_privilege")

    # 🔻 Drop constraints using batch mode (required for SQLite)
    with op.batch_alter_table("role_privilege", schema=None) as batch_op:
        batch_op.drop_constraint("fk_role_privilege_privilege_id", type_="foreignkey")
        batch_op.drop_constraint("fk_role_privilege_role_id", type_="foreignkey")
        batch_op.drop_constraint("uq_role_privilege", type_="unique")
        batch_op.drop_constraint("pk_role_privilege_id", type_="primary")

    # 🔻 Drop the table
    op.drop_table("role_privilege")


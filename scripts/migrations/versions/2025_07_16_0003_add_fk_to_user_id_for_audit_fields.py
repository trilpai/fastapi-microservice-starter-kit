"""Add FK constraints for audit fields (created_by, updated_by) referencing `user.id`.

Revision ID: 35d024da8e2e
Revises: 1f89f8e4a935
Create Date: 2025-07-16 15:07:24.755789
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = '35d024da8e2e'
down_revision: Union[str, Sequence[str], None] = '1f89f8e4a935'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add foreign key constraints to audit fields (created_by, updated_by) across key tables."""
    # ➕ privilege.audit_fields → user.id
    with op.batch_alter_table("privilege") as batch_op:
        batch_op.create_foreign_key(
            "fk_privilege_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_privilege_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # ➕ role.audit_fields → user.id
    with op.batch_alter_table("role") as batch_op:
        batch_op.create_foreign_key(
            "fk_role_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_role_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # ➕ role_privilege.audit_fields → user.id
    with op.batch_alter_table("role_privilege") as batch_op:
        batch_op.create_foreign_key(
            "fk_role_privilege_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_role_privilege_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # 🔁 user.audit_fields (self-referencing) → user.id
    with op.batch_alter_table("user") as batch_op:
        batch_op.create_foreign_key(
            "fk_user_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_user_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )


def downgrade() -> None:
    """Remove FK constraints on audit fields."""
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_constraint("fk_user_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_updated_by", type_="foreignkey")

    with op.batch_alter_table("role_privilege") as batch_op:
        batch_op.drop_constraint("fk_role_privilege_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_role_privilege_updated_by", type_="foreignkey")

    with op.batch_alter_table("role") as batch_op:
        batch_op.drop_constraint("fk_role_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_role_updated_by", type_="foreignkey")

    with op.batch_alter_table("privilege") as batch_op:
        batch_op.drop_constraint("fk_privilege_created_by", type_="foreignkey")
        batch_op.drop_constraint("fk_privilege_updated_by", type_="foreignkey")

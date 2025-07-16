"""add FK to user.id for audit fields

Revision ID: 35d024da8e2e
Revises: 1f89f8e4a935
Create Date: 2025-07-16 15:07:24.755789
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '35d024da8e2e'
down_revision: Union[str, Sequence[str], None] = '1f89f8e4a935'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with batch mode for cross-dialect FK support."""
    # Add FKs to `privilege`
    with op.batch_alter_table("privilege", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_privilege_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_privilege_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # Add FKs to `role`
    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_role_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_role_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # Add FKs to `role_privilege`
    with op.batch_alter_table("role_privilege", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_role_privilege_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_role_privilege_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )

    # Add self-referencing FKs to `user`
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_user_created_by", "user", ["created_by"], ["id"], ondelete="SET NULL"
        )
        batch_op.create_foreign_key(
            "fk_user_updated_by", "user", ["updated_by"], ["id"], ondelete="SET NULL"
        )


def downgrade() -> None:
    """Downgrade schema by removing FKs using batch mode."""
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_user_created_by", type_="foreignkey")

    with op.batch_alter_table("role_privilege", schema=None) as batch_op:
        batch_op.drop_constraint("fk_role_privilege_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_role_privilege_created_by", type_="foreignkey")

    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.drop_constraint("fk_role_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_role_created_by", type_="foreignkey")

    with op.batch_alter_table("privilege", schema=None) as batch_op:
        batch_op.drop_constraint("fk_privilege_updated_by", type_="foreignkey")
        batch_op.drop_constraint("fk_privilege_created_by", type_="foreignkey")

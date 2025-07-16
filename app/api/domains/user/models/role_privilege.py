# app/api/domains/user/models/role_privilege.py

"""
🔗 Join table for Role–Privilege many-to-many mapping.

Each row connects a `Role` with a `Privilege`, forming a bridge between
user access levels and the actions they're allowed to perform.

Supports:
- Many-to-many relationships between `role` and `privilege`
- Unique constraint to prevent duplicate mappings
- Soft-delete and audit trail via `TimestampMixin`
"""

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


# -------------------------------------
# 🔗 RolePrivilege Join Table Definition
# -------------------------------------
class RolePrivilege(Base, TimestampMixin):
    """
    The `role_privilege` table implements a many-to-many join
    between `role` and `privilege`.

    - A role can have multiple privileges.
    - A privilege can belong to multiple roles.
    - No duplicate pairs allowed (enforced via unique constraint).
    """

    __tablename__ = "role_privilege"

    __table_args__ = (
        # 🚫 Ensure each role–privilege pair is unique
        UniqueConstraint("role_id", "privilege_id", name="uq_role_privilege"),
        # ✅ Support soft-deletion queries
        Index("ix_role_privilege_deleted_at", "deleted_at"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID for this role–privilege mapping",
    )

    # 🔗 FK to role table
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the `role` this privilege is assigned to",
    )

    # 🔗 FK to privilege table
    privilege_id: Mapped[int] = mapped_column(
        ForeignKey("privilege.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the `privilege` assigned to the role",
    )

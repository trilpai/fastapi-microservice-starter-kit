# app/api/domains/user/models/role_privilege.py

"""
Database model for the many-to-many relationship between roles and privileges.

Each row represents a mapping of a single privilege to a role, supporting
fine-grained access control across the system.
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
    The `role_privilege` table links roles to privileges in a many-to-many fashion.

    A role can have many privileges, and a privilege can belong to many roles.
    """

    __tablename__ = "role_privilege"

    __table_args__ = (
        UniqueConstraint("role_id", "privilege_id", name="uq_role_privilege"),
        Index("ix_role_privilege_deleted_at", "deleted_at"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Primary key ID"
    )

    # 🔗 FK to Role
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE"),
        nullable=False,
        doc="FK to role table",
    )

    # 🔗 FK to Privilege
    privilege_id: Mapped[int] = mapped_column(
        ForeignKey("privilege.id", ondelete="CASCADE"),
        nullable=False,
        doc="FK to privilege table",
    )

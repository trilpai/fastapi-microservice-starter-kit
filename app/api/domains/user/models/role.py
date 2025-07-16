# app/api/domains/user/models/role.py

"""
🛡️ Database model for user roles.

Each `Role` is a named bundle of access rights (privileges) such as:
- Admin
- Viewer
- Staff

Roles are assigned to users, and they define what parts of the system
a user can access or modify, via many-to-many links to `Privilege`.

Supports:
- Unique role names
- Soft-deletion for audit-friendly revocation
- Backrefs to associated users and privileges
"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

# 🔁 Forward imports to avoid circular references at runtime
if TYPE_CHECKING:
    from app.api.domains.user.models.privilege import Privilege
    from app.api.domains.user.models.user import User


# --------------------------
# 🛡️ Role Table Definition
# --------------------------
class Role(Base, TimestampMixin):
    """
    The `role` table defines named collections of access privileges.

    Each role:
    - Has a unique name (e.g., 'Admin', 'Manager')
    - Can be assigned to multiple users
    - Maps to multiple privileges (via `role_privilege` join table)

    Roles provide a coarse-grained layer of access control.
    """

    __tablename__ = "role"

    __table_args__ = (
        # ✅ Used to efficiently filter soft-deleted roles
        Index("ix_role_deleted_at", "deleted_at"),
    )

    # 🔑 Primary key — unique identifier for the role
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Primary key ID for the role"
    )

    # 🏷️ Unique name of the role (e.g., 'SuperAdmin', 'Editor')
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        doc="Unique role name (e.g., 'Admin', 'Viewer')",
    )

    # 📝 Optional textual description to explain the role
    description: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True,
        doc="Optional description of this role's responsibilities",
    )

    # 🔁 Many-to-many relationship: roles ↔ privileges
    privileges: Mapped[List["Privilege"]] = relationship(
        "Privilege",
        secondary="role_privilege",
        back_populates="roles",
        lazy="selectin",
        doc="List of privileges assigned to this role",
    )

    # 🔄 One-to-many relationship: role → users
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="role",
        lazy="selectin",
        doc="Users assigned to this role",
    )

    # 📋 Utility: List of privilege names associated with this role
    @property
    def privilege_names(self) -> List[str]:
        """
        Returns a list of all privilege names attached to this role.
        Useful for display and authorization checks.
        """
        return [priv.name for priv in self.privileges]

# app/api/domains/user/models/role.py

"""
Database model for user roles.

Each role is a named grouping of privileges (e.g., "Admin", "Manager", "Viewer")
that can be assigned to users to control access in the system.
"""

from typing import Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


# --------------------------
# 🛡️ Role Table Definition
# --------------------------
class Role(Base, TimestampMixin):
    """
    The `role` table defines named groups of privileges
    that can be assigned to users for access control.

    Examples: "SuperAdmin", "Moderator", "Viewer"
    """

    __tablename__ = "role"

    # ✅ Index for soft-deletion filtering
    __table_args__ = (
        Index("ix_role_deleted_at", "deleted_at"),
    )

    # 🔑 Unique identifier for each role
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID"
    )

    # 🏷️ Unique name for the role (e.g., 'Admin', 'Staff')
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        doc="Unique role name (e.g., 'SuperAdmin')"
    )

    # 📝 Optional role description
    description: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True,
        doc="Optional description of the role"
    )

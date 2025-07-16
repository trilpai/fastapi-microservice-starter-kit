# app/api/domains/user/models/privilege.py

"""
🔐 Database model for system privileges.

A privilege represents a named permission or access control unit
(e.g., "read_reports", "edit_users"). Privileges are assigned to
roles (many-to-many) which in turn are granted to users.

This model supports:
- Soft deletion with `deleted_at`
- Many-to-many mapping to `Role` via the `role_privilege` join table
- Optional descriptions for better admin UI clarity
"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

# Forward declaration to avoid circular imports during model load
if TYPE_CHECKING:
    from app.api.domains.user.models.role import Role


# -----------------------------
# 🔐 Privilege Table Definition
# -----------------------------
class Privilege(Base, TimestampMixin):
    """
    The `privilege` table defines fine-grained access rights in the system.

    These privileges are not granted directly to users, but assigned to `Role`,
    which can be linked to multiple users. For example:
    - "create_user"
    - "delete_invoice"
    - "view_audit_logs"

    This model supports unique names, optional descriptions, and is
    soft-deletable for long-term auditing.
    """

    __tablename__ = "privilege"

    __table_args__ = (
        # ✅ Index to allow fast filtering of soft-deleted rows
        Index("ix_privilege_deleted_at", "deleted_at"),
    )

    # 🔑 Primary Key — auto-incremented integer
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Primary key ID for the privilege"
    )

    # 🏷️ Name of the privilege — must be unique
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        doc="Unique identifier for the privilege (e.g., 'view_dashboard')",
    )

    # 📝 Optional human-readable description (used in admin UI or docs)
    description: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True,
        doc="Optional description explaining the permission's purpose",
    )

    # 🔁 Many-to-many relationship to `Role`
    # Implemented via join table: `role_privilege`
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="role_privilege",
        back_populates="privileges",
        lazy="selectin",
        doc="List of roles that include this privilege",
    )

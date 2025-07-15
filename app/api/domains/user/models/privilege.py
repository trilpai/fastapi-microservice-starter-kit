# app/api/domains/user/models/privilege.py

"""
Database model for user privileges.

Represents access rights (like "read_reports", "edit_users", etc.)
associated with roles or users in the system.
"""

from typing import Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


# -----------------------------
# 🔐 Privilege Table Definition
# -----------------------------
class Privilege(Base, TimestampMixin):
    """
    The `privilege` table stores named access rights in the system,
    which can be mapped to roles or directly to users for fine-grained access control.

    Example privileges: "create_user", "delete_invoice", "view_dashboard"
    """

    __tablename__ = "privilege"

    # ✅ Add index for soft-deletion queries
    __table_args__ = (
        Index("ix_privilege_deleted_at", "deleted_at"),
    )

    # 🔑 Unique identifier for each privilege
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID"
    )

    # 🏷️ Unique name of the privilege (e.g., 'manage_users')
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        doc="Unique name of the privilege (e.g., 'view_reports')"
    )

    # 📝 Optional human-readable description
    description: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True,
        doc="Optional description of what this privilege allows"
    )

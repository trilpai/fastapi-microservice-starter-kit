# app/database/mixins.py

"""
🔁 Shared SQLAlchemy Mixin for Audit Fields

This module defines a reusable TimestampMixin class that:
- Adds standardized timestamp and user attribution fields to any model
- Enables soft-deletion via `deleted_at`
- Ensures consistent auditability across all tables in your database
- Designed for SQLAlchemy 2.0-style `Mapped` annotations
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


# --------------------------------------
# 🧱 Mixin for Timestamps & Audit Fields
# --------------------------------------
class TimestampMixin:
    """
    Mixin class for common audit fields used in almost every table.

    Includes:
    - created_at: auto-set on INSERT
    - updated_at: auto-updated on UPDATE
    - created_by / updated_by: optional user tracking
    - deleted_at: optional soft-delete timestamp

    Usage:
        class MyModel(Base, TimestampMixin):
            ...
    """

    # ✅ Timestamp when the record was created (set once on insert)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="Timestamp when the record was created"
    )

    # 🔁 Timestamp when the record was last updated (auto-updates on UPDATE)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when the record was last updated"
    )

    # 👤 Optional user ID of the creator
    created_by: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="User ID of the record creator"
    )

    # 🛠️ Optional user ID of the last modifier
    updated_by: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="User ID of the last record updater"
    )

    # 🗑️ If set, the record is considered soft-deleted
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        doc="Soft-delete marker; timestamp when the record was logically deleted"
    )

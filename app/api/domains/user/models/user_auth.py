# app/api/domains/user/models/user_auth.py

"""
📛 Database model for user authentication.

The `user_auth` table manages credentials and authentication metadata for individual users.

Features:
- Optional username-based login
- Secure password storage using bcrypt/argon2
- Account lockout support after repeated failures
- Tracks last successful login
- Full audit trail and soft-delete support via TimestampMixin
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin


# -------------------------------------------
# 🔐 UserAuth Table Definition (Login Details)
# -------------------------------------------
class UserAuth(Base, TimestampMixin):
    """
    The `user_auth` table stores credentials and authentication metadata for users.

    It supports:
    - Optional username-based login
    - Hashed password storage (bcrypt/argon2)
    - Account lockout on repeated failed attempts
    - Tracking of last login timestamp
    - Soft-deletion and auditing via `TimestampMixin`
    """

    __tablename__ = "user_auth"

    # ✅ Index for soft-deletion filtering
    __table_args__ = (Index("ix_user_auth_deleted_at", "deleted_at"),)

    # 🔑 Unique ID for each login record
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID for each authentication record",
    )

    # 🔗 Reference to the associated user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the associated user (deletes on cascade)",
    )

    # 👤 Optional username for login (can be email/mobile elsewhere)
    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        doc="Optional unique username for login (can be null if not used)",
    )

    # 🔒 Hashed password (bcrypt, argon2, etc.)
    password_hash: Mapped[str] = mapped_column(
        String(256), nullable=False, doc="Securely hashed user password"
    )

    # 🚫 Number of consecutive failed password attempts
    wrong_password_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
        doc="Number of failed password attempts (used to trigger lockouts)",
    )

    # ⏳ Lockout expiry time (if user is locked out after repeated failures)
    account_locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp until which the account is locked (if locked out)",
    )

    # 📅 Last successful login time
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of the user's last successful login",
    )

    # ↩️ SQLAlchemy relationship (optional backref to User)
    user = relationship(
        "User",
        backref="auth",
        lazy="joined",
        doc="Back-reference to the owning user",
    )

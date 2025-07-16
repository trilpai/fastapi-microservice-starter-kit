# app/api/domains/user/models/user_auth.py

"""
🔐 Database model for user authentication credentials.

The `user_auth` table handles login credentials and related metadata,
such as:
- Username-based login (optional, fallback to identity table possible)
- Hashed password storage (bcrypt, argon2, etc.)
- Lockout protection after failed login attempts
- Timestamp of last successful login
- Soft-deletion and auditing via TimestampMixin

Each user has at most one associated `user_auth` record (1:1 relationship).
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

# 🔁 Forward reference to avoid circular import
if TYPE_CHECKING:
    from app.api.domains.user.models.user import User


# ---------------------------------------
# 🧾 UserAuth Table Definition (1:1 Login)
# ---------------------------------------
class UserAuth(Base, TimestampMixin):
    """
    The `user_auth` table stores login credentials and metadata for users.

    It includes:
    - Optional username for login (if not using email/mobile only)
    - Secure password hash (bcrypt, argon2, etc.)
    - Account lockout fields
    - Last login tracking
    """

    __tablename__ = "user_auth"

    __table_args__ = (
        # ✅ For filtering soft-deleted login records
        Index("ix_user_auth_deleted_at", "deleted_at"),
        # ✅ For quickly resolving user ID lookups (foreign key)
        Index("ix_user_auth_user_id", "user_id"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID for each authentication record",
    )

    # 🔗 FK to user (CASCADE on delete)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the associated user (deletes on cascade)",
    )

    # 👤 Optional unique username for login
    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        doc="Optional unique username for login (nullable if not used)",
    )

    # 🔒 Password hash (bcrypt, argon2, etc.)
    password_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        doc="Hashed user password using a secure algorithm",
    )

    # 🚫 Wrong login attempt counter
    wrong_password_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
        doc="Count of consecutive failed login attempts",
    )

    # ⏳ Lockout window after too many failures
    account_locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Time until which the account remains locked after failures",
    )

    # 📅 Timestamp of last successful login
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of user's last successful login",
    )

    # ↩️ Relationship to user (1:1)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="auth",
        lazy="joined",
        doc="Back-reference to the owning user (1:1)",
    )

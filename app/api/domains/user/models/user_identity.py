# app/api/domains/user/models/user_identity.py

"""
🆔 Database model for user identities.

Each user can have multiple identities such as email addresses, mobile numbers,
or third-party OAuth UIDs. Identities support:
- Verification status (OTP or OAuth)
- Primary identity designation (e.g., primary email or phone)
- OTP-based login and rate-limiting
- Soft-deletion and full audit trail
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

# 🔁 Avoid circular imports during runtime
if TYPE_CHECKING:
    from app.api.domains.user.models.user import User


# ----------------------------
# 📛 Enum for Identity Types
# ----------------------------
class IdentityType(str, Enum):
    EMAIL = "email"
    MOBILE = "mobile"
    OAUTH = "oauth"


# -----------------------------------------------
# 📇 UserIdentity Table Definition (email/mobile)
# -----------------------------------------------
class UserIdentity(Base, TimestampMixin):
    """
    The `user_identity` table stores one or more identity records
    for each user (email, phone number, or OAuth UID).

    Each identity supports:
    - Type-specific uniqueness
    - Verification and OTP support
    - Primary designation (used for contact/login)
    """

    __tablename__ = "user_identity"

    __table_args__ = (
        # 🚫 Ensure uniqueness across identity types and providers
        UniqueConstraint("type", "value", "oauth_provider", name="uq_identity_value"),
        # ✅ Soft-deletion index
        Index("ix_user_identity_deleted_at", "deleted_at"),
        # ⚡ Indexed flags for filtering
        Index("ix_user_identity_is_verified", "is_verified"),
        Index("ix_user_identity_is_primary", "is_primary"),
        # 🔗 Fast lookup for identities belonging to a user
        Index("ix_user_identity_user_id", "user_id"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID of the identity record",
    )

    # 🔗 Foreign key to the owning user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the user who owns this identity",
    )

    # 🧾 Identity type: email / mobile / oauth
    type: Mapped[IdentityType] = mapped_column(
        SQLEnum(IdentityType, name="identity_type"),
        nullable=False,
        doc="Type of identity: email, mobile, or oauth",
    )

    # 🔤 Email address, phone number, or OAuth UID
    value: Mapped[str] = mapped_column(
        String(191),
        nullable=False,
        doc="Actual identity value (email address, phone number, or OAuth UID)",
    )

    # ✅ Whether this identity has been verified (OTP or OAuth)
    is_verified: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        server_default="0",
        doc="Indicates whether the identity has been verified",
    )

    # ⭐ Marks the preferred contact identity (e.g., primary email or mobile)
    is_primary: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        server_default="0",
        doc="True if this is the user's primary contact identity",
    )

    # 🌐 Required only if type = 'oauth' (e.g., google, github, facebook)
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, doc="OAuth provider name if type is 'oauth'"
    )

    # 🔐 OTP used for verification (mobile/email)
    otp_code: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, doc="Last OTP code sent to this identity"
    )

    otp_generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when the last OTP was generated",
    )

    wrong_otp_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
        doc="Count of wrong OTP entries for rate-limiting",
    )

    otp_locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Time until OTP entry is locked due to failures",
    )

    # ↩️ Relationship to the User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="identities",
        lazy="joined",
        doc="Back-reference to the owning user",
    )

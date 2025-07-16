# app/api/domains/user/models/user_identity.py

"""
Database model for user identities.

Represents verified or unverified identity records (email, mobile, or OAuth UID)
linked to a user. Supports OTP-based verification, lockout tracking, and
primary identity designation.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

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


# ---------------------------
# 🧾 Enum for Identity Type
# ---------------------------
class IdentityType(str, Enum):
    EMAIL = "email"
    MOBILE = "mobile"
    OAUTH = "oauth"


# --------------------------------------
# 🆔 UserIdentity Table Definition
# --------------------------------------
class UserIdentity(Base, TimestampMixin):
    """
    The `user_identity` table stores one or more identity types
    associated with a user — email, mobile, or OAuth identity.

    - Used for login, communication, and OTP flows
    - Tracks whether identity is verified
    - Flags primary identities (e.g., primary email)
    """

    __tablename__ = "user_identity"

    # ✅ Soft delete index
    __table_args__ = (
        UniqueConstraint("type", "value", "oauth_provider", name="uq_identity_value"),
        Index("ix_user_identity_deleted_at", "deleted_at"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Primary key ID",
    )

    # 🔗 Link to owning user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the associated user",
    )

    # 📛 Type: email / mobile / oauth
    type: Mapped[IdentityType] = mapped_column(
        SQLEnum(IdentityType, name="identity_type"),
        nullable=False,
        doc="Type of identity: email, mobile, or oauth",
    )

    # 🔤 Identity value (email address, phone number, or UID)
    value: Mapped[str] = mapped_column(
        String(191),
        nullable=False,
        doc="Actual identity value (email, phone, or OAuth UID)",
    )

    # ✅ Verification status
    is_verified: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        server_default="0",
        doc="Whether this identity has been verified (OTP or OAuth)",
    )

    # ⭐ Preferred identity for contact/login
    is_primary: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        server_default="0",
        doc="Is this the user's primary email/mobile (default contact)?",
    )

    # 🌐 Provider for OAuth identity (required if type = oauth)
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="OAuth provider (e.g., google, facebook) if identity type is oauth",
    )

    # 🔢 OTP-related fields
    otp_code: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        doc="Last generated OTP for verification (mobile/email)",
    )
    otp_generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when the OTP was generated",
    )
    wrong_otp_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
        doc="Number of wrong OTP attempts",
    )
    otp_locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Account locked until this time after OTP failures",
    )

    # 🔁 Relationship to user
    user = relationship(
        "User", back_populates="identities", lazy="joined", doc="Owner of this identity"
    )

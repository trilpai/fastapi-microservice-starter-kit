# app/api/domains/user/models/user.py

"""
Database model for users in the system.

Stores core user profile data, including identity fields (names, DOB, gender),
role assignment, and metadata required for login and audit tracking.
"""

from datetime import date
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Index, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin


# --------------------------
# ⚧️ Gender Enum Declaration
# --------------------------
class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


# ----------------------
# 👤 User Table Definition
# ----------------------
class User(Base, TimestampMixin):
    """
    The `user` table holds the core user information.

    Linked to role (authorization), and extended via user_identity and user_auth tables.
    """

    __tablename__ = "user"

    __table_args__ = (Index("ix_user_deleted_at", "deleted_at"),)

    # 🔑 Primary Key
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Primary key ID"
    )

    # 🧑 First Name (required)
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False, doc="First name of the user"
    )

    # 👩 Last Name (optional)
    last_name: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, doc="Last name of the user"
    )

    # 💼 Job title (e.g., Software Developer)
    job_title: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, doc="Optional job title or designation"
    )

    # ⚧️ Gender (enum)
    gender: Mapped[Optional[Gender]] = mapped_column(
        SQLAEnum(Gender), nullable=True, doc="Gender identity (enum)"
    )

    # 🎂 Date of Birth
    dob: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, doc="Date of birth"
    )

    # 🖼️ Profile Picture URL
    profile_image_url: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True, doc="URL or path to profile image"
    )

    # ✅ Active Flag
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="1",  # SQLite uses TEXT, but this works across dialects
        doc="Is the user currently active?",
    )

    # 🔗 Role FK
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK to assigned role",
    )

    # 🆔 One-to-many relationship to UserIdentity
    identities = relationship(
        "UserIdentity",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="List of all email/mobile/oauth identities",
    )

# app/api/domains/user/models/user.py

"""
👤 Database model for system users.

Stores core user profile information, including name, gender, DOB,
profile image, role assignment, and links to login credentials and
communication identities.

Supports:
- One-to-many link to user_identity (email/mobile/oauth)
- One-to-one link to user_auth (login credentials)
- Foreign key to role (authorization)
- Audit trail and soft-delete via TimestampMixin
"""

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Index, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

# --------------------------------------------
# 🔁 Forward references to avoid circular import
# --------------------------------------------
if TYPE_CHECKING:
    from app.api.domains.user.models.role import Role
    from app.api.domains.user.models.user_auth import UserAuth
    from app.api.domains.user.models.user_identity import UserIdentity


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
    The `user` table holds essential profile and authorization data,
    and connects to:
    - `user_identity`: for communication (email/mobile/OAuth)
    - `user_auth`: for credentials and login control
    - `role`: for access rights and privilege inheritance
    """

    __tablename__ = "user"

    __table_args__ = (
        # ✅ For soft-deletion-aware queries
        Index("ix_user_deleted_at", "deleted_at"),
        # ✅ To support filtered queries by role and status
        Index("ix_user_role_id", "role_id"),
        Index("ix_user_is_active", "is_active"),
    )

    # 🔑 Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Primary key ID"
    )

    # 🙍 First name (required)
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False, doc="User's first name"
    )

    # 👨 Last name (optional)
    last_name: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, doc="User's last name (optional)"
    )

    # 💼 Job title or designation (optional)
    job_title: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, doc="Optional job title or designation"
    )

    # ⚧️ Gender enum (optional)
    gender: Mapped[Optional[Gender]] = mapped_column(
        SQLAEnum(Gender), nullable=True, doc="User's gender (enum, optional)"
    )

    # 🎂 Date of birth (optional)
    dob: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, doc="Date of birth"
    )

    # 🖼️ Profile image URL (optional)
    profile_image_url: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True, doc="URL or path to profile image"
    )

    # ✅ Active flag
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="1",
        doc="Whether the user is active in the system",
    )

    # 🔗 FK to Role (not nullable)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="RESTRICT"),
        nullable=False,
        doc="Foreign key to assigned role",
    )

    # 🔁 Many-to-one: user.role → Role.users
    role: Mapped["Role"] = relationship(
        "Role", back_populates="users", lazy="joined", doc="Assigned role object"
    )

    # 🔐 One-to-one: user.auth ↔ UserAuth.user
    auth: Mapped[Optional["UserAuth"]] = relationship(
        "UserAuth",
        back_populates="user",
        uselist=False,
        lazy="joined",
        doc="Authentication credentials object",
    )

    # 🆔 One-to-many: user.identities ↔ UserIdentity.user
    identities: Mapped[List["UserIdentity"]] = relationship(
        "UserIdentity",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="List of email/mobile/OAuth identities",
    )

    # 📋 Derived list of privilege names
    @property
    def privilege_names(self) -> List[str]:
        """
        Returns a list of all privilege names granted to this user via their role.
        """
        return self.role.privilege_names if self.role else []

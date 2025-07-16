# app/database/base.py

"""
Shared SQLAlchemy Declarative Base for all models.

This module defines a common `Base` class that:
- Serves as the parent for all SQLAlchemy ORM models
- Centralizes metadata collection for Alembic autogeneration
- Ensures Alembic "sees" all models via explicit imports
"""

from sqlalchemy.orm import DeclarativeBase


# --------------------------------------
# 🚩 Universal Base class for all models
# --------------------------------------
class Base(DeclarativeBase):
    """
    SQLAlchemy Declarative Base.

    All models in the project should inherit from this.
    It stores the metadata needed for migrations and schema reflection.
    """

    pass


# --------------------------------------
# 🧩 Import all models here to register with Alembic
# --------------------------------------
# Important: This is required for Alembic to "see" all models when autogenerating migrations.
# Without this import, Alembic won't detect your models automatically.
from app.api.domains.user.models.privilege import Privilege
from app.api.domains.user.models.role import Role
from app.api.domains.user.models.role_privilege import RolePrivilege

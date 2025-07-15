# app/database/base.py
from sqlalchemy.orm import DeclarativeBase

from app.api.domains.user.models.privilege import Privilege


class Base(DeclarativeBase):
    pass

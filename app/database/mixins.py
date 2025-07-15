# app/database/mixins.py
from typing import Optional

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_by: Mapped[Optional[Integer]] = mapped_column(nullable=True)
    updated_by: Mapped[Optional[Integer]] = mapped_column(nullable=True)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(nullable=True)

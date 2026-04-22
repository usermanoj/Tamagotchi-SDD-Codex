from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), default="ChuChu")
    hunger: Mapped[int] = mapped_column(Integer, default=92)
    happiness: Mapped[int] = mapped_column(Integer, default=92)
    energy: Mapped[int] = mapped_column(Integer, default=92)
    status: Mapped[str] = mapped_column(String(20), default="normal")
    last_reaction: Mapped[str] = mapped_column(String(255), default="ChuChu is awake and curious.")
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    healthy_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_ticks: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

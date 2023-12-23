import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(30), unique=True)
    money_per_hour: Mapped["UserMoneyPerHour"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    working_days: Mapped[List["WorkingDay"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserMoneyPerHour(Base):
    __tablename__ = "user_money_per_hour"

    id: Mapped[int] = mapped_column(primary_key=True)
    money_per_hour: Mapped[float] = mapped_column(Float())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="money_per_hour")


class WorkingDay(Base):
    __tablename__ = "working_day"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime())
    hours: Mapped[float] = mapped_column(Float())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="working_days")

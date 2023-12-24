from datetime import datetime

from aiogram import types
from sqlalchemy import select, update

from database.engine import get_session
from database.models import User, UserMoneyPerHour, WorkingDay


async def add_user(message: types.Message):
    user_id = message.from_user.id

    session = await get_session()
    user = User(user_id=str(user_id))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await session.close()


async def get_user_from_db(message: types.Message):
    session = await get_session()
    statement = select(User).filter(
        User.user_id == str(message.from_user.id)
    )
    result = await session.execute(statement)
    user = result.scalar_one()
    await session.close()
    return user


async def set_money_per_hour_to_db(message: types.Message, user: User):
    session = await get_session()
    money_per_hour_object = await session.execute(
        select(
            UserMoneyPerHour
        ).filter(
            UserMoneyPerHour.user_id == user.id
        )
    )
    result = money_per_hour_object.scalar_one_or_none()
    if not result:
        money_per_hour = UserMoneyPerHour(
            money_per_hour=float(message.text), user_id=user.id
        )
        session.add(money_per_hour)
    else:
        statement = update(UserMoneyPerHour).values(
            money_per_hour=float(message.text)
        ).where(UserMoneyPerHour.user_id == user.id)
        await session.execute(statement)
    await session.commit()
    await session.close()


async def add_working_day(message: types.Message, date: dict, hours: float):
    date_to_datetime = datetime(
        year=date["year"],
        month=date["month"],
        day=date["day"],
    )

    user = await get_user_from_db(message)

    session = await get_session()
    working_day = WorkingDay(
        date=date_to_datetime,
        hours=hours,
        user_id=user.id
    )

    session.add(working_day)
    await session.commit()
    await session.refresh(working_day)
    await session.close()

from typing import Any

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.db_utils import add_working_day, get_user_from_db, \
    set_money_per_hour_to_db

create_router = Router(name=__name__)


class Form(StatesGroup):
    year = State()
    month = State()
    day = State()
    money_per_hour = State()
    hours = State()


@create_router.message(Command("add_working_day_data"))
@create_router.message(F.text.casefold() == "add_working_day_data")
async def chose_working_year(message: types.Message, state: FSMContext):
    await state.set_state(Form.year)
    await message.answer(
        f"Введіть рік.",
    )


@create_router.message(Form.year)
async def chose_working_month(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(Form.month)
    await message.answer(
        "Введіть число місяця.",
    )


@create_router.message(Form.month)
async def chose_working_day(message: types.Message, state: FSMContext):
    await state.update_data(month=message.text)
    await state.set_state(Form.day)
    await message.answer(
        "Введіть число дня.",
    )


@create_router.message(Form.day)
async def add_hours(message: types.Message, state: FSMContext):
    await state.update_data(day=message.text)
    await state.set_state(Form.hours)
    await message.answer(
        "Введіть кількість відпрацьованих годин.",
    )


@create_router.message(Form.hours)
async def successful_adding_data(message: types.Message, state: FSMContext):
    data = await state.update_data(hours=message.text)
    await state.clear()
    await show_summary(message, data)


async def show_summary(message: types.Message, data: dict[str, Any]):
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    date = f"{year}-{month}-{day}"
    hours = data.get("hours")

    date_dict = {
        "year": int(year),
        "month": int(month),
        "day": int(day),
    }

    await add_working_day(message, date_dict, float(hours))

    await message.answer(
        f"За дату {date} відпрацьовано {hours} год."
    )


@create_router.message(Command("set_salary_per_hour"))
@create_router.message(F.text.casefold() == "set_salary_per_hour")
async def handle_salary_per_hour(message: types.Message, state: FSMContext):
    await state.set_state(Form.money_per_hour)
    await message.answer(
        "Введіть суму, яку ви отримуєте за годину."
    )


@create_router.message(Form.money_per_hour)
async def set_money_per_hour(message: types.Message, state: FSMContext):
    user = await get_user_from_db(message)
    await set_money_per_hour_to_db(message, user)

    await message.answer(
        f"Налаштування погодинної оплати встановлено на {message.text} євро."
    )
    await state.clear()

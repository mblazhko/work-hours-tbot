from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.db_utils import add_user

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    user_name = message.from_user.full_name
    await add_user(message)
    await message.answer(f"Привіт {user_name}! Щоб додати дані будь ласка виберіть в меню відповідну команду.")

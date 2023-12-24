from aiogram import Dispatcher, Bot
from .routers import start_router, create_router
from aiogram.enums import ParseMode
from config import BOT_TOKEN

dp = Dispatcher()


async def run_bot():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp.include_routers(start_router, create_router)
    await dp.start_polling(bot)

import asyncio
import sys

from aiogram import Bot, Dispatcher

from src.handlers.user_handlers.algorithm import router_algorithm
from src.config import settings


async def main():

    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    dp.include_router(router_algorithm)

    print("Бот успешно запущен!", file=sys.stderr)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


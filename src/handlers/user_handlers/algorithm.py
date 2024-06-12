import json

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError

from src.algorithm.algorithm import algorithm
from src.db import DB_MONGO

router_algorithm = Router()


@router_algorithm.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(
        text=f"Hi, <a href='{message.from_user.url}'>{message.from_user.username}</a>!",
        parse_mode="html",
    )


@router_algorithm.message()
async def process_algorithm(message: Message):
    try:
        data = json.loads(message.text)
        dates, months = algorithm(
            dt_from=data["dt_from"],
            dt_upto=data["dt_upto"],
            group_type=data["group_type"],
        )
        result = DB_MONGO.get_data_using_algorithm(
            group_type=data["group_type"],
            dates=dates,
        )
        await message.answer(
            text=f"{repr(result)}"
        )
    except (Exception, TelegramAPIError):
        await message.answer(
            text="Невалидный запрос. Пример запроса:\n"
                 '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}',
        )

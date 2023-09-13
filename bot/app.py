import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.db_manager import DBmanager
from env_conf import BOT_TOKEN, DB_PARAMS
from finance import Finance
from keyboards import *
from utils import check_add_template, get_today_finance_message, get_today_edit

# Setting bot up
TOKEN = BOT_TOKEN

# Creating routers
base_router = Router(name="base_router")
show_stats_router = Router(name="statistics_router")

# Database manager
db_manager = DBmanager(**DB_PARAMS)


@base_router.message(CommandStart())
async def command_start(message: Message):
    await message.answer("Приветствую!",
                         reply_markup=start_keyboard.as_markup(resize_keyboard=True))


@base_router.message(F.text.casefold() == "финансы сегодня")
async def show_finance_today(message: Message):
    data = db_manager.select_today_query()
    reply_message = get_today_finance_message(*data)
    await message.answer(reply_message,
                         parse_mode=ParseMode.HTML,
                         reply_markup=ask_edit_keyboard.as_markup(resize_keyboard=True))


@base_router.message(F.text.casefold() == "редактировать")
async def show_finance_today(message: Message):
    data = db_manager.select_today_query()

    list_income, list_expenses = get_today_edit(*data)

    for fin in list_income:
        await message.answer(fin,
                             reply_markup=generate_inline_edit_keyboard(fin).as_markup())

    for fin in list_expenses:
        await message.answer(fin,
                             reply_markup=generate_inline_edit_keyboard(fin).as_markup())


@base_router.message()
async def add_finance(message: Message):
    if check_add_template(message.text)[0]:
        finance = Finance()
        finance.set_attrs_by_list_param(*check_add_template(message.text))
        db_manager.insert_query(finance)
        reply_message = "<b>Расходы обновлены</b>"

        if finance.get_isincome():
            reply_message = "<b>Доходы обновлены</b>"

        await message.answer(f"{reply_message}",
                             reply_markup=start_keyboard.as_markup(resize_keyboard=True))


async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(base_router, show_stats_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

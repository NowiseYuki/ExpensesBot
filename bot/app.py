import asyncio
import logging
import sys

from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from utils import DialogSM, Spending, start_keyboard, cancel_keyboard

from db.db_manager import DBmanager
from env_conf import BOT_TOKEN, DB_PARAMS

# Setting bot up
TOKEN = BOT_TOKEN

# Creating routers
add_spending_router = Router(name="add_spending_router")
show_stats_router = Router(name="statistics_router")

# Database manager
db_manager = DBmanager(**DB_PARAMS)


@add_spending_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!",
                         reply_markup=start_keyboard.as_markup(resize_keyboard=True))


@show_stats_router.message(F.text.casefold() == "просмотреть статистику")
async def show_statistics(message: Message):
    data = db_manager.select_query(param=0)
    await message.answer(
        f"{data}"
    )


@add_spending_router.message(F.text.casefold() == "отменить операцию")
async def cancel_operation(message: Message, state):
    await state.clear()
    await message.answer(
        "Операция успешно отменена!",
        reply_markup=start_keyboard.as_markup(resize_keyboard=True),
    )


@add_spending_router.message(F.text.casefold() == "добавить трату")
async def add_spending(message: Message, state: FSMContext):
    await state.set_state(DialogSM.title)
    await message.answer(
        "Введите название траты",
        reply_markup=cancel_keyboard.as_markup(resize_keyboard=True)
    )


@add_spending_router.message(DialogSM.title)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(DialogSM.price)
    await message.answer(
        "Отлично! Теперь введите сумму в долларах",
        reply_markup=cancel_keyboard.as_markup(resize_keyboard=True)
    )


@add_spending_router.message(DialogSM.price)
async def ask_about_date(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(DialogSM.date_guess)
    await message.answer(
        "Трата была совершена только что?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="да"),
                    KeyboardButton(text="нет"),
                    KeyboardButton(text="Отменить операцию")
                ]
            ],
            resize_keyboard=True,
        )
    )


# Yes
@add_spending_router.message(DialogSM.date_guess, F.text.casefold() == "да")
async def auto_date(message: Message, state: FSMContext):
    await save_spending(message, state)


# No (step 1)
@add_spending_router.message(DialogSM.date_guess, F.text.casefold() == "нет")
async def enter_date(message: Message, state: FSMContext):
    await state.set_state(DialogSM.enter_date)

    await message.answer(
        "Пожалуйста, введите дату в формате:\n"
        "День.Месяц\n"
        "Например - 10.09",
        reply_markup=cancel_keyboard.as_markup(resize_keyboard=True),
    )


# No (step 2)
@add_spending_router.message(DialogSM.enter_date)
async def save_date(message: Message, state: FSMContext):
    await state.update_data(enter_date=message.text)
    await save_spending(message, state)


# Если вместо Да/Нет было написано что-либо ещё
@add_spending_router.message(DialogSM.date_guess)
async def process_wrong_answer(message: Message):
    if message.text not in ['да', 'нет']:
        await message.reply("Введите либо 'Да', либо 'Нет'",
                            reply_markup=cancel_keyboard.as_markup(resize_keyboard=True))


# Save data
async def save_spending(message: Message, state):
    data = await state.get_data()
    await state.clear()

    spending_obj = Spending(data["description"], data["price"])
    try:
        if data["enter_date"]:
            spending_obj.set_dt(data["enter_date"])
    except KeyError:
        print("Дата не была обновлена")

    db_manager.insert_query(spending_obj)
    await message.answer(
        "Траты успешно обновлены!",
        reply_markup=start_keyboard.as_markup(resize_keyboard=True),
    )


async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(add_spending_router, show_stats_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

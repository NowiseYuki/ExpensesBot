from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import date, time, datetime


# Start Keyboard
start_keyboard = ReplyKeyboardBuilder()
start_keyboard.button(text=f"Добавить трату")
start_keyboard.button(text=f"Просмотреть статистику")

# Cancel Keyboard
cancel_keyboard = ReplyKeyboardBuilder()
cancel_keyboard.button(text=f"Отменить операцию")


# Dialog State Machine
class DialogSM(StatesGroup):
    title = State()
    price = State()
    date_guess = State()
    enter_date = State()


# Spenging object
class Spending:
    def __init__(self, description: str = "", price: int = 0):
        self.description: str = description
        self.price: int = price
        self.dt: datetime = datetime.now()

    def __str__(self):
        return (f"\n{self.description}\n"
                f"{self.price}\n"
                f"{self.dt}\n")

    # Доделать проверки для данных
    def set_dt(self, dt: str):
        year: int = datetime.now().year
        day, month = dt.split('.')
        date_: date = date(year, int(month), int(day))
        time_: time = time(0, 0, 0, 0)
        self.dt: datetime = datetime.combine(date_, time_)

    def get_params(self):
        return self.description, self.price, self.dt


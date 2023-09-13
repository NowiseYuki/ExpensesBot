import datetime
import re

from finance import Finance


def check_add_template(message) -> tuple[list, int]:
    """
    Checks user's message with reg_ex and defines
    how much pieces it should be devided.
    Created for formatting user input.
    :param
        message: user's message
    :return:
        tuple:
            list: message splitted by ',' delimeter
            int: param that defines number of divided pieces
    """
    r_ex_3 = '^[+,-]?\d+,\w+,\w+'
    r_ex_2 = '^[+,-]?\d+,\w+'
    r_ex_1 = '^[+,-]?\d+'
    r_ex_list = [r_ex_3, r_ex_2, r_ex_1]

    for index, r_ex in enumerate(r_ex_list):
        if re.search(r_ex, message):
            return message.split(','), 3 - index
    return [], 0


def list_to_finances(list_):
    fin_list = []
    for tuple_ in list_:
        fin_list.append(Finance(*tuple_))
    return fin_list


def get_sum_amount(list_):
    amount = 0
    for fin in list_:
        amount += fin.get_amount()
    return amount


def list_into_message(list_):
    message = ""
    for fin in list_:
        message += f"{fin.str_for_message()}\n"


def get_today_edit(list_income, list_expenses):
    list_income: list = list_to_finances(list_income)
    list_expenses: list = list_to_finances(list_expenses)

    for i in range(len(list_income)):
        list_income[i] = list_income[i].str_for_message()

    for i in range(len(list_expenses)):
        list_expenses[i] = list_expenses[i].str_for_message()

    return list_income, list_expenses


def get_today_finance_message(list_income, list_expenses):
    list_income: list = list_to_finances(list_income)
    list_expenses: list = list_to_finances(list_expenses)

    income_amount: int = get_sum_amount(list_income)
    expenses_amount: int = get_sum_amount(list_expenses)

    message = (f"{datetime.date.today()}\nФинансы за сегодня\n\n"
               f"Доходы ({income_amount}):\n")

    for fin in list_income:
        message += fin.str_for_message() + "\n"

    message += f"\nРасходы (-{expenses_amount}):\n"

    for fin in list_expenses:
        message += fin.str_for_message() + "\n"

    message += f"\nИтог: {income_amount - expenses_amount}"
    return message

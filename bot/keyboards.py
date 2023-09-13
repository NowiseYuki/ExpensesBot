from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Start Keyboard
start_keyboard = ReplyKeyboardBuilder()
start_keyboard.button(text=f"Финансы сегодня")
start_keyboard.button(text=f"Мои финансы")
start_keyboard.button(text=f"?")

# Ask Edit
ask_edit_keyboard = ReplyKeyboardBuilder()
ask_edit_keyboard.button(text="Редактировать")
ask_edit_keyboard.attach(start_keyboard)

# Inline Edit
edit_keyboard = InlineKeyboardBuilder()
edit_keyboard.button(text="Изменить", callback_data='Edit')
edit_keyboard.button(text="Удалить", callback_data='Remove')
edit_keyboard.adjust(1, 2)


def generate_inline_edit_keyboard(fin_obj):
    edit_kbd = InlineKeyboardBuilder()
    edit_kbd.button(text="Изменить", callback_data=f'edit_{fin_obj}')
    edit_kbd.button(text="Удалить", callback_data=f'remove_{fin_obj}')
    edit_kbd.adjust(1, 2)
    return edit_kbd

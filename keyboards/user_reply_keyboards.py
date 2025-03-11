from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

user_keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Программа 📢")],
        [KeyboardButton(text="Пройти опрос 📊")],
        [KeyboardButton(text="Задать вопрос 💬")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбирите действие:",
    selective=True,
)

user_keyboard_ask_question = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Спикеру 👔"),
            KeyboardButton(text="Администрации 🎩"),
        ],
        [KeyboardButton(text="Назад ⬅️")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберете кому хотите задать вопрос:",
    selective=True,
)

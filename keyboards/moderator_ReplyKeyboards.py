from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

moderator_keyboard_main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать конференцию")]],
    resize_keyboard=True,
    selective=True,
)

moderator_keyboard_conference = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Перейти к следующему спикеру")],
        [KeyboardButton(text="Завершить конференцию")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=True,
)

moderator_keyboard_in_develop = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Данная функция в разработке",
    one_time_keyboard=True,
    selective=True,
)

# Импорты
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

admin_keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать конференцию")],
        [KeyboardButton(text="Настройки конференции")],
        [KeyboardButton(text="Отправить рассылку")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие:",
    selective=True,
)

admin_keyboard_settings = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменить название")],
        [KeyboardButton(text="Ввести опрос")],
        [KeyboardButton(text="Ввести данные о спикерах")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие:",
    selective=True,
)

admin_keyboard_conference = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Перейти к следующему спикеру")],
        [KeyboardButton(text="Завершить конференцию")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=True,
)

admin_keyboard_in_develop = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Данная функция в разработке",
    one_time_keyboard=True,
    selective=True,
)

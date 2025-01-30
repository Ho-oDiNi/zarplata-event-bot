# Импорты
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

user_keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить информацию")],
        [KeyboardButton(text="Задать вопрос")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбирите действие:",
    selective=True,
)

user_keyboard_ask_question = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Текущему спикеру"),
            KeyboardButton(text="Конкретному спикеру"),
        ],
        [KeyboardButton(text="Администрации")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберете кому хотите задать вопрос:",
    selective=True,
)


def user_keyboard_builder_speakers():
    conference_speakers = get_conference_speakers()
    builder = ReplyKeyboardBuilder()
    for speaker in conference_speakers:
        builder.button(text=f"{speaker}")
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


user_keyboard_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить"),
            KeyboardButton(text="Отмена"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True,
)

user_keyboard_in_develop = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Данная функция в разработке",
    one_time_keyboard=True,
    selective=True,
)

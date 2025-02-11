from config.bot_config import MANAGER
from aiogram.utils.keyboard import *
from utils.db_requests import *


def user_keyboard_builder_feedback():
    builder = InlineKeyboardBuilder()
    builder.button(text="Связаться с администратором", url=f"tg://user?id={MANAGER}")

    return builder.as_markup()


def user_keyboard_builder_speakers():
    builder = InlineKeyboardBuilder()
    event_speakers = get_event_speakers()

    for speaker in event_speakers:
        builder.button(
            text=f"{speaker['name']}",
            callback_data=f"ask_speaker?id={speaker['id']}",
        )
    builder.adjust(2)

    return builder.as_markup(one_time_keyboard=True)


def user_keyboard_quiz():
    builder = InlineKeyboardBuilder()
    builder.button(text="Поехали", callback_data="start_quiz")

    return builder.as_markup()


user_keyboard_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить", callback_data="send_question")],
        [InlineKeyboardButton(text="Отмена", callback_data="none")],
    ]
)

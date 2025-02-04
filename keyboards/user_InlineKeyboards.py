from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.requests import *


def user_keyboard_builder_feedback():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Связаться с администратором", url=f"tg://user?id={get_management_id()}"
    )

    return builder.as_markup()


def user_keyboard_builder_speakers():

    builder = InlineKeyboardBuilder()
    conference_speakers = get_conference_speakers()

    builder.button(
        text=f"Текущему спикеру", callback_data="ask_current_speaker", width=1
    )
    for speaker in conference_speakers:
        builder.button(text=f"{speaker['name']}", callback_data="ask_concrete_speaker")
    builder.adjust(1, 2)

    return builder.as_markup(one_time_keyboard=True)

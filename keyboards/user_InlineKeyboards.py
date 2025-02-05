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
        text=f"Текущему спикеру",
        callback_data=f"ask_speaker?id={get_current_speaker()['id']}",
        width=1,
    )
    for speaker in conference_speakers:
        builder.button(
            text=f"{speaker['name']}",
            callback_data=f"ask_speaker?id={speaker['id']}",
        )
    builder.adjust(1, 2)

    return builder.as_markup(one_time_keyboard=True)


def user_keyboard_survey():
    builder = InlineKeyboardBuilder()
    builder.button(text="Поехали", callback_data="start_survey")

    return builder.as_markup()

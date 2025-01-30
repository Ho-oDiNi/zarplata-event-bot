from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_keyboard_builder_feedback():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Связаться с администратором", url=f"tg://user?id={get_admin_id()}"
    )

    return builder.as_markup()

from aiogram.utils.keyboard import *
from utils.db_requests import *

admin_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать Ивент", callback_data="change_event")],
        [InlineKeyboardButton(text="Создать Ивент", callback_data="create_event")],
    ]
)


def admin_keyboard_builder_events():
    builder = InlineKeyboardBuilder()
    for event in get_nearest_events():
        builder.button(
            text=f"{event['name']}",
            callback_data=f"current_event?id={event['id']}",
        )

    builder.button(text="В меню", callback_data="menu")

    builder.adjust(2, 1)
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_quizes(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить опрос", callback_data=f"in_develop")
    builder.button(text="Копировать опрос", callback_data=f"in_develop")
    for quiz in get_event_quizes(event_id):
        builder.button(
            text=f"{quiz['name']}",
            callback_data=f"current_quiz?id={quiz['id']}",  # &event_id={event_id}
        )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(2)
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_speakers(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить спикера", callback_data=f"in_develop")
    for speaker in get_event_speakers(event_id):
        builder.button(
            text=f"{speaker['name']}",
            callback_data=f"current_speaker?id={speaker['id']}",  # &event_id={event_id}
        )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(1, 2)
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_setting(event_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Настройки ивента",
        callback_data=f"setting_event?id={event_id}",
    )
    builder.button(
        text="Настройки опроса",
        callback_data=f"setting_survey?id={event_id}",
    )
    builder.button(
        text="Настройки спикеров",
        callback_data=f"setting_speaker?id={event_id}",
    )
    builder.button(
        text="Переключить таблицу",
        callback_data=f"change_table?id={event_id}",
    )
    builder.button(
        text="Отправить рассылку",
        callback_data=f"send_mailing?id={event_id}",
    )
    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data="change_event")

    builder.adjust(3, 2, 2)
    return builder.as_markup()


def admin_keyboard_builder_event(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить название", callback_data=f"change_name?id={event_id}"
    ),
    builder.button(
        text="Изменить описание", callback_data=f"change_content?id={event_id}"
    ),
    builder.button(text="Сменить дату", callback_data=f"change_date?id={event_id}"),
    builder.button(text="Сменить фото", callback_data=f"change_photo?id={event_id}"),

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(2)
    return builder.as_markup()


def admin_keyboard_setting_quiz(quiz_id, event_id=2):
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить варианты", callback_data=f"in_develop")
    builder.button(text="Изменить название", callback_data=f"in_develop")
    builder.button(text="Изменить описание", callback_data=f"in_develop")
    builder.button(text="Сменить фото", callback_data=f"in_develop")

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"setting_survey?id={event_id}")

    builder.adjust(2)
    return builder.as_markup()


def admin_keyboard_setting_speaker(speaker_id, event_id=2):
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить имя", callback_data=f"in_develop")
    builder.button(text="Изменить описание", callback_data=f"in_develop")
    builder.button(text="Сменить фото", callback_data=f"in_develop")
    builder.button(text="Назад", callback_data=f"setting_speaker?id={event_id}")

    builder.adjust(2)
    return builder.as_markup()


admin_keyboard_in_develop = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад")]],
)

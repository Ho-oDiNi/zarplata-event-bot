from aiogram.utils.keyboard import *
from utils.db_requests import *
from utils.parsers import *


def admin_keyboard_main():
    current_event = get_current_event()
    if current_event is not None:
        current_event_id = current_event["id"]
    else:
        current_event_id = None

    builder = InlineKeyboardBuilder()
    builder.button(
        text="К текущему Ивенту", callback_data=f"current_event?id={current_event_id}"
    )
    builder.button(text="Выбрать Ивент", callback_data="change_event")
    builder.button(
        text="Создать Ивент",
        callback_data="pre_create_row?table=events&field=name&id=_",
    )

    builder.button(
        text="Отправить рассылку",
        callback_data=f"pre_mass_mailing",
    )
    builder.button(
        text="Переключить гугл таблицу",
        callback_data=f"pre_change_table",
    )

    builder.adjust(1, 2, 2)
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_events(callback):
    builder = InlineKeyboardBuilder()
    nearest_events = get_nearest_events()
    for event in nearest_events:
        builder.button(
            text=f"{event['name']}",
            callback_data=f"{callback}?id={event['id']}",
        )

    builder.button(text="В меню", callback_data="menu")

    builder.adjust(*parse_button(middle=len(nearest_events), end=1))
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_quizes(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Создать квиз",
        callback_data=f"pre_create_row?table=quizes&field=name&id={event_id}",
    )
    builder.button(
        text="Копировать квизы",
        callback_data=f"pre_copy_quiz?table=_&field=_&id={event_id}",
    )

    event_quizes = get_event_quizes(event_id)
    for quiz in event_quizes:
        builder.button(
            text=f"{quiz['name']}",
            callback_data=f"current_quiz?id={quiz['id']}",
        )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(*parse_button(start=2, middle=len(event_quizes), end=2))
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_variants(quiz_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить вариант",
        callback_data=f"pre_create_row?table=variants&field=name&id={quiz_id}",
    )
    quiz_variants = get_quiz_variants(quiz_id)
    for variant in quiz_variants:
        builder.button(
            text=f"{variant['name']}",
            callback_data=f"current_variant?id={variant['id']}",
        )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_quiz?id={quiz_id}")

    builder.adjust(*parse_button(start=1, middle=len(quiz_variants), end=2))
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_builder_speakers(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить спикера",
        callback_data=f"pre_create_row?table=speakers&field=name&id={event_id}",
    )
    event_speakers = get_event_speakers(event_id)
    for speaker in event_speakers:
        builder.button(
            text=f"{speaker['name']}",
            callback_data=f"current_speaker?id={speaker['id']}",
        )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(*parse_button(start=1, middle=len(event_speakers), end=2))
    return builder.as_markup(one_time_keyboard=True)


def admin_keyboard_setting(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Настройки ивента",
        callback_data=f"setting_event?id={event_id}",
    )
    builder.button(
        text="Настройки квизов",
        callback_data=f"setting_survey?id={event_id}",
    )
    builder.button(
        text="Настройки спикеров",
        callback_data=f"setting_speaker?id={event_id}",
    )
    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data="change_event")

    builder.adjust(1, 2, 2)
    return builder.as_markup()


def admin_keyboard_builder_event(event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить название",
        callback_data=f"pre_change_row?table=events&field=name&id={event_id}",
    )
    builder.button(
        text="Изменить описание",
        callback_data=f"pre_change_row?table=events&field=content&id={event_id}",
    )
    builder.button(
        text="Сменить фото",
        callback_data=f"pre_change_row?table=events&field=img&id={event_id}",
    )
    builder.button(
        text="Сменить дату",
        callback_data=f"pre_change_row?table=events&field=date&id={event_id}",
    )
    builder.button(
        text="Удалить Ивент",
        callback_data=f"pre_delete_row?table=events&field=_&id={event_id}",
    )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"current_event?id={event_id}")

    builder.adjust(2, 2, 1, 2)
    return builder.as_markup()


def admin_keyboard_setting_quiz(quiz_id, event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Настройки ответов", callback_data=f"setting_variants?id={quiz_id}"
    )

    builder.button(
        text="Изменить название",
        callback_data=f"pre_change_row?table=quizes&field=name&id={quiz_id}",
    )
    builder.button(
        text="Изменить описание",
        callback_data=f"pre_change_row?table=quizes&field=content&id={quiz_id}",
    )
    builder.button(
        text="Сменить фото",
        callback_data=f"pre_change_row?table=quizes&field=img&id={quiz_id}",
    )

    builder.button(
        text="Удалить Квиз",
        callback_data=f"pre_delete_row?table=quizes&field=_&id={event_id}",
    )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Назад", callback_data=f"setting_survey?id={event_id}")

    builder.adjust(1, 3, 1, 2)
    return builder.as_markup()


def admin_keyboard_setting_variant(variant_id, quiz_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить название",
        callback_data=f"pre_change_row?table=variants&field=name&id={variant_id}",
    )
    builder.button(
        text="Изменить результаты",
        callback_data=f"pre_change_row?table=variants&field=result&id={variant_id}",
    )
    builder.button(
        text="Удалить ответ",
        callback_data=f"pre_delete_row?table=variants&field=_&id={variant_id}",
    )

    builder.button(text="В меню", callback_data="menu")
    builder.button(text=f"Назад", callback_data=f"current_quiz?id={quiz_id}")

    builder.adjust(2, 1, 2)
    return builder.as_markup()


def admin_keyboard_setting_speaker(speaker_id, event_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить имя",
        callback_data=f"pre_change_row?table=speakers&field=name&id={speaker_id}",
    )
    builder.button(
        text="Изменить описание",
        callback_data=f"pre_change_row?table=speakers&field=content&id={speaker_id}",
    )
    builder.button(
        text="Сменить фото",
        callback_data=f"pre_change_row?table=speakers&field=img&id={speaker_id}",
    )
    builder.button(
        text="Удалить Спикера",
        callback_data=f"pre_delete_row?table=speakers&field=_&id={event_id}",
    )
    builder.button(text="Назад", callback_data=f"setting_speaker?id={event_id}")
    builder.button(text="В меню", callback_data="menu")

    builder.adjust(3, 1, 2)
    return builder.as_markup()


admin_keyboard_in_develop = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад")]],
)


def admin_keyboard_confirm(callback):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data=f"{callback}")],
            [InlineKeyboardButton(text="Отмена", callback_data="none")],
        ]
    )


admin_keyboard_cancel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="none")]],
)

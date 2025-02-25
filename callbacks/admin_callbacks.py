from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.admin_reply_keyboards import *
from keyboards.admin_inline_keyboards import *
from filters.admin_filter import *
from utils.states import Admin
from utils.parsers import *


router = Router()
router.message.filter(IsAdminFilter())


@router.callback_query(F.data == "change_event")
async def change_event(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите ивент",
        reply_markup=admin_keyboard_builder_events("current_event"),
    )


@router.callback_query(F.data == "pre_mass_mailing")
async def pre_mass_mailing(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите ивент для рассылки",
        reply_markup=admin_keyboard_builder_events("prepare_mailing"),
    )


@router.callback_query(F.data == "pre_change_table")
async def pre_change_table(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите ивент для отображения",
        reply_markup=admin_keyboard_builder_events("prepare_change_table"),
    )


@router.callback_query(F.data.startswith("prepare_change_table"))
async def pre_change_table(callback: CallbackQuery, bot: Bot, state: FSMContext):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await state.update_data(requestId=event["id"])
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Вы уверены, что хотите сменить таблицу?\n\nВНИМАНИЕ!\n\nПроцессс занимает МНОГО времени",
        reply_markup=admin_keyboard_confirm("change_table"),
    )


@router.callback_query(F.data == "change_table")
async def pre_change_table(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Дождитесь окончания процесса!",
    )

    adminState = await state.get_data()
    bot.google_table.changeTable(adminState["requestId"])

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно завершено",
        reply_markup=admin_keyboard_main(),
    )


@router.callback_query(F.data.startswith("current_event"))
async def on_current_event(callback: CallbackQuery, bot: Bot):
    event_id = callback.data.partition("id=")[2]
    if event_id == "None":
        await bot.send_message(
            chat_id=callback.from_user.id, text=f"Сейчас нет активных Ивентов"
        )
        return

    event = get_by_id("events", event_id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбрана конференция {event["name"]}",
        reply_markup=admin_keyboard_setting(event["id"]),
    )


@router.callback_query(F.data.startswith("current_quiz"))
async def on_current_quiz(callback: CallbackQuery, bot: Bot):
    quiz = get_by_id(
        "quizes",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбран опрос {quiz["name"]}",
        reply_markup=admin_keyboard_setting_quiz(quiz["id"], quiz["event_id"]),
    )


@router.callback_query(F.data.startswith("current_variant"))
async def on_current_variant(callback: CallbackQuery, bot: Bot):
    variant = get_by_id(
        "variants",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбран вариант {variant["name"]}",
        reply_markup=admin_keyboard_setting_variant(variant["id"], variant["quiz_id"]),
    )


@router.callback_query(F.data.startswith("current_speaker"))
async def on_current_speaker(callback: CallbackQuery, bot: Bot):
    speaker = get_by_id(
        "speakers",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбран спикер {speaker["name"]}",
        reply_markup=admin_keyboard_setting_speaker(speaker["id"], speaker["event_id"]),
    )


@router.callback_query(F.data.startswith("setting_event"))
async def setting_event(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Внесите изменение в ивенте {event["name"]}",
        reply_markup=admin_keyboard_builder_event(event["id"]),
    )


@router.callback_query(F.data.startswith("setting_survey"))
async def setting_survey(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите опрос для {event["name"]}",
        reply_markup=admin_keyboard_builder_quizes(event["id"]),
    )


@router.callback_query(F.data.startswith("setting_speaker"))
async def setting_speaker(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите спикера для {event["name"]}",
        reply_markup=admin_keyboard_builder_speakers(event["id"]),
    )


@router.callback_query(F.data.startswith("setting_variants"))
async def setting_variants(callback: CallbackQuery, bot: Bot):
    quiz = get_by_id(
        "quizes",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите вариант ответов для {quiz["name"]}",
        reply_markup=admin_keyboard_builder_variants(quiz["id"]),
    )


@router.callback_query(F.data.startswith("prepare_mailing"))
async def prepare_mailing(callback: CallbackQuery, bot: Bot, state: FSMContext):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )

    await state.update_data(requestId=event["id"])
    await state.set_state(Admin.massMailing)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Введите сообщение рассылки для пользователей {event["name"]}",
        reply_markup=admin_keyboard_cancel,
    )


@router.callback_query(F.data == "send_mailing")
async def send_mailing(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()
    for user in get_event_users(adminState["requestId"]):
        try:
            await bot.send_photo_if_exist(
                chat_id=user["tg_id"],
                caption=f"{adminState["addPhoto"]}",
                text=f"{adminState["massMailing"]}",
            )
        except:
            print(f"Чат {user["tg_id"]} не доступен")

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно доставлено",
        reply_markup=admin_keyboard_main(),
    )
    await state.clear()


@router.callback_query(F.data.startswith("pre_change_row"))
async def pre_change_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback_table, callback_field, callback_id = parse_callback_data(callback.data)

    await state.update_data(requestTable=callback_table)
    await state.update_data(requestField=callback_field)
    await state.update_data(requestId=callback_id)

    data = get_by_id(callback_table, callback_id)

    await state.set_state(Admin.changeRow)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Введите новое значение {callback_field} для {data["name"]}",
        reply_markup=admin_keyboard_cancel,
    )


@router.callback_query(F.data.startswith("pre_delete_row"))
async def pre_delete_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback_table, _, callback_id = parse_callback_data(callback.data)

    await state.update_data(requestTable=callback_table)
    await state.update_data(requestId=callback_id)

    data = get_by_id(callback_table, callback_id)

    await state.set_state(Admin.deleteRow)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Вы уверены, что хотите удалить {data["name"]}?",
        reply_markup=admin_keyboard_confirm("delete_row"),
    )


@router.callback_query(F.data.startswith("delete_row"))
async def delete_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()
    delete_by_id(adminState["requestTable"], adminState["requestId"])
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно удалено",
        reply_markup=admin_keyboard_main(),
    )
    await state.clear()


@router.callback_query(F.data.startswith("pre_create_row"))
async def pre_create_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback_table, callback_field, callback_id = parse_callback_data(callback.data)

    await state.update_data(requestTable=callback_table)
    await state.update_data(requestField=callback_field)
    await state.update_data(requestId=callback_id)
    await state.set_state(Admin.createRow)

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Введите название для поля",
        reply_markup=admin_keyboard_cancel,
    )


@router.callback_query(F.data.startswith("create_row"))
async def create_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()

    row_id = insert_row(
        adminState["requestTable"],
        adminState["requestField"],
        adminState["createRow"],
    )

    FK_field = parse_FK_field(adminState["requestTable"])
    if FK_field:
        update_by_id(
            adminState["requestTable"],
            FK_field,
            row_id,
            adminState["requestId"],
        )

        next_cell = parse_next_cell(
            adminState["requestTable"], FK_field, adminState["requestId"]
        )
        update_by_id(
            adminState["requestTable"],
            "cell",
            row_id,
            next_cell,
        )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно создано, хотите создать еще?",
        reply_markup=admin_keyboard_confirm(
            f"pre_create_row?table={adminState["requestTable"]}&field={adminState["requestField"]}&id={adminState["requestId"]}"
        ),
    )
    await state.clear()


@router.callback_query(F.data == "change_row")
async def change_row(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()

    update_by_id(
        adminState["requestTable"],
        adminState["requestField"],
        adminState["requestId"],
        adminState["changeRow"],
    )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно изменено",
        reply_markup=admin_keyboard_main(),
    )
    await state.clear()


@router.callback_query(F.data.startswith("pre_copy_quiz"))
async def pre_copy_quiz(callback: CallbackQuery, bot: Bot, state: FSMContext):
    _, _, callback_id = parse_callback_data(callback.data)

    await state.update_data(requestId=callback_id)
    await state.set_state(Admin.copyQuiz)

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите ивент, с которого хотитие скопировать опрос",
        reply_markup=admin_keyboard_builder_events("copy_quiz"),
    )


@router.callback_query(F.data.startswith("copy_quiz"))
async def copy_quiz(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()

    copy_quiz_by_id(adminState["requestId"], callback.data.partition("id=")[2])

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно изменено",
        reply_markup=admin_keyboard_main(),
    )
    await state.clear()


@router.callback_query(F.data == "admin_menu")
async def move_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Меню ивентов",
        reply_markup=admin_keyboard_main(),
    )


@router.callback_query(F.data == "admin_none")
async def cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Действие отменено",
        reply_markup=admin_keyboard_main(),
    )

    await state.clear()


@router.callback_query(F.data == "in_develop")
async def test(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id, text=f"Функция в разработке")

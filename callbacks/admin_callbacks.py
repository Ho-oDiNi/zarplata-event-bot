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
        text=f"Ивенты за два месяца",
        reply_markup=admin_keyboard_builder_events(),
    )


@router.callback_query(F.data.startswith("current_event"))
async def on_current_event(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбрана конференция {event["name"]}",
        reply_markup=admin_keyboard_setting(event["id"]),
    )


@router.callback_query(F.data.startswith("current_quiz"))
async def on_current_event(callback: CallbackQuery, bot: Bot):
    quiz = get_by_id(
        "quizes",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбран опрос {quiz["name"]}",
        reply_markup=admin_keyboard_setting_quiz(quiz["id"], quiz["event_id"]),
    )


@router.callback_query(F.data.startswith("current_speaker"))
async def on_current_event(callback: CallbackQuery, bot: Bot):
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
async def test(callback: CallbackQuery, bot: Bot):
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
async def test(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбирите спикера для {event["name"]}",
        reply_markup=admin_keyboard_builder_speakers(event["id"]),
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
            await bot.send_message(
                chat_id=user["tg_id"],
                text=f"{adminState["massMailing"]}",
            )
        except:
            print(f"Чат {user["tg_id"]} не доступен")
        finally:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f"Успешно доставлено",
            )
            await state.clear()


@router.callback_query(F.data.startswith("prepare_field"))
async def prepare_field(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback_table, callback_field, callback_id = parse_callback_data(callback.data)

    await state.update_data(requestTable=callback_table)
    await state.update_data(requestField=callback_field)
    await state.update_data(requestId=callback_id)

    data = get_by_id(callback_table, callback_id)

    await state.set_state(Admin.changeField)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Введите новое значение {callback_field} для {data["name"]}",
        reply_markup=admin_keyboard_cancel,
    )


@router.callback_query(F.data == "change_field")
async def change_field(callback: CallbackQuery, bot: Bot, state: FSMContext):
    adminState = await state.get_data()

    update_by_id(
        adminState["requestTable"],
        adminState["requestField"],
        adminState["requestId"],
        adminState["changeField"],
    )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Успешно изменено",
        reply_markup=admin_keyboard_main,
    )
    await state.clear()


@router.callback_query(F.data == "menu")
async def move_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выберете действие:",
        reply_markup=admin_keyboard_main,
    )


@router.callback_query(F.data == "none")
async def cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Действие отменено",
        reply_markup=admin_keyboard_main,
    )

    await state.clear()


@router.callback_query(F.data == "in_develop")
async def test(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id, text=f"Функция в разработке")

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.admin_reply_keyboards import *
from keyboards.admin_inline_keyboards import *
from filters.admin_filter import *

router = Router()
router.message.filter(IsAdminFilter())


@router.callback_query(F.data == "change_event")
async def change_event(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Ивенты за два месяца:",
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
        text=f"Выбрана конференция {event["name"]}:",
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
        text=f"Выбран опрос {quiz["name"]}:",
        reply_markup=admin_keyboard_setting_quiz(quiz["id"]),
    )


@router.callback_query(F.data.startswith("current_speaker"))
async def on_current_event(callback: CallbackQuery, bot: Bot):
    speaker = get_by_id(
        "speakers",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выбран спикер {speaker["name"]}:",
        reply_markup=admin_keyboard_setting_speaker(speaker["id"]),
    )


@router.callback_query(F.data.startswith("setting_event"))
async def setting_event(callback: CallbackQuery, bot: Bot):
    event = get_by_id(
        "events",
        callback.data.partition("id=")[2],
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Внесите изменение в ивенте {event["name"]}:",
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
        text=f"Выбирите опрос для {event["name"]}:",
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
        text=f"Выбирите спикера для {event["name"]}:",
        reply_markup=admin_keyboard_builder_speakers(event["id"]),
    )


@router.callback_query(F.data == "menu")
async def move_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Выберете действие:",
        reply_markup=admin_keyboard_main,
    )


@router.callback_query(
    F.data == "in_develop"
    or F.data.startswith("change_table")
    or F.data.startswith("send_mailing")
    or F.data.startswith("change")
)
async def test(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id, text=f"Функция в разработке")

# Импорты
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.user_ReplyKeyboards import *
from keyboards.user_InlineKeyboards import *

router = Router()


@router.message(F.text.lower().in_({"назад", "меню"}))
@router.message(Command("menu", "start"))
async def user_handler_menu(message: Message):
    await message.answer(
        text=f"Привет, {message.from_user.id}, рады видеть на конференции НАЗВАНИЕ",
        reply_markup=user_keyboard_main,
    )


@router.message(F.text.lower() == "получить информацию")
async def user_handler_get_info(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    # conference_info = get_conference_info()
    await message.answer(text=f"В РАЗРАБОТКЕ")


@router.message(F.text.lower() == "задать вопрос")
async def user_handler_ask_question(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=user_keyboard_ask_question)


@router.message(F.text.lower() == "текущему спикеру")
async def user_handler_ask_current_speaker(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=user_keyboard_in_develop)


@router.message(F.text.lower() == "конкретному спикеру")
async def user_handler_ask_concrete_speaker(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"В РАЗРАБОТКЕ", reply_markup=user_keyboard_builder_speakers()
    )


@router.message(F.text.lower() == "администрации")
async def user_handler_ask_admin(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"В РАЗРАБОТКЕ", reply_markup=user_keyboard_builder_feedback()
    )


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

from aiogram import Router, F, Bot
from aiogram.types import Message, URLInputFile
from aiogram.filters import Command
from keyboards.user_ReplyKeyboards import *
from keyboards.user_InlineKeyboards import *

router = Router()


@router.message(F.text.lower().in_({"назад", "меню"}))
@router.message(Command("menu", "start"))
async def user_handler_menu(message: Message):
    db_set_user(message.from_user.id)
    await message.answer(
        text=f"Привет, {message.from_user.first_name}, рады видеть на конференции {get_current_conference()['name']}",
        reply_markup=user_keyboard_main,
    )


@router.message(F.text.lower() == "о конференции")
async def user_handler_get_info(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(text=f"{get_current_conference()['description']}")
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=URLInputFile(get_current_conference()["content"]),
    )


@router.message(F.text.lower() == "пройти опрос")
async def user_handler_get_info(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(text=f"Вы готовы начать?", reply_markup=user_keyboard_survey())


@router.message(F.text.lower() == "задать вопрос")
async def user_handler_ask_question(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"Кому Вы хотите задать вопрос?", reply_markup=user_keyboard_ask_question
    )


@router.message(F.text.lower() == "спикеру")
async def user_handler_ask_speaker(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"Выберете спикера",
        reply_markup=user_keyboard_builder_speakers(),
    )


@router.message(F.text.lower() == "администрации")
async def user_handler_ask_management(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"Задайте любой интересующий Вас вопрос",
        reply_markup=user_keyboard_builder_feedback(),
    )


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

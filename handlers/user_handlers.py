from aiogram import Router, F, Bot
from aiogram.types import Message, URLInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.user_ReplyKeyboards import *
from keyboards.user_InlineKeyboards import *
from utils.states import User

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


@router.message(User.question)
async def user_handler_confirm_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(User.confirm)
    await message.answer(
        text=f"Подтвердите отправку вопроса:\n{message.text}",
        reply_markup=user_keyboard_confirm,
    )


@router.message(User.confirm)
async def user_handler_send_question(message: Message, state: FSMContext, bot: Bot):
    userState = await state.get_data()
    if message.text.lower() == "отправить":
        await bot.send_message(
            chat_id=get_management_id(),
            text=f"Для {userState['speaker']} вопрос: {userState['question']}\n ",
        )
        await message.answer(text=f"Вопрос отправлен модератору")

    else:
        await message.answer(text=f"Действие отменено")

    await state.clear()


@router.message()
async def error_message(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

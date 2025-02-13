from aiogram import Router, F, Bot
from aiogram.types import Message, URLInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from filters.event_filter import HasEventFilter
from utils.states import User

router = Router()
router.message.filter((HasEventFilter()))


@router.message(Command("start", "restart"))
async def user_handler_menu(message: Message, bot: Bot):
    set_user(message.from_user.id)
    await message.answer(
        text=f"Привет, {message.from_user.first_name}, рады видеть на конференции {get_current_event()['name']}",
        reply_markup=user_keyboard_main,
    )
    await user_handler_info(message, bot)


@router.message(F.text.lower().in_({"назад", "меню", "о конференции"}))
@router.message(Command("menu"))
async def user_handler_info(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=URLInputFile(get_current_event()["img"]),
            caption=f"{get_current_event()['content']}",
            reply_markup=user_keyboard_main,
        )
    except:
        await message.answer(
            text=f"{get_current_event()['content']}",
            reply_markup=user_keyboard_main,
        )


@router.message(F.text.lower() == "пройти опрос")
async def user_handler_quiz(message: Message, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await message.answer(
        text=f"Вы готовы начать?", reply_markup=user_keyboard_survey_start
    )


@router.message(F.text.lower() == "задать вопрос")
async def user_handler_question(message: Message, bot: Bot):
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
async def user_handler_confirm(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(
        text=f"Подтвердите отправку вопроса:\n{message.text}",
        reply_markup=user_keyboard_confirm,
    )


@router.message()
async def error_message(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

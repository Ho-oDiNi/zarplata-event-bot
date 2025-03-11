from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from filters.event_filter import HasEventFilter
from utils.registers import *
from utils.states import User
from config.bot_config import IMG

router = Router()
router.message.filter((HasEventFilter()))


@router.message(Command("start", "restart", "Start", "Restart"))
async def user_handler_menu(message: Message, bot: Bot):
    set_user(message.from_user.id)
    await bot.send_photo_if_exist(
        chat_id=message.chat.id,
        caption=get_current_event()["img"],
        text=get_current_event()["content"],
        reply_markup=user_keyboard_main,
    )

    await user_handler_info(message, bot)


@router.message(
    F.text.lower().in_({"назад ⬅️", "программа 📢", "назад", "программа", "меню"})
)
@router.message(Command("menu", "Menu"))
async def user_handler_info(message: Message, bot: Bot):
    try:
        await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    except:
        print("Message not found")

    await bot.send_chat_action(message.from_user.id, action="typing")
    msg = await bot.send_document_if_exist(
        chat_id=message.chat.id,
        document=get_current_event()["document"],
        reply_markup=user_keyboard_main,
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message(F.text.lower().in_({"пройти опрос 📊", "пройти опрос"}))
async def user_handler_quiz(message: Message, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")

    if get_by_tg_id(message.from_user.id)["is_passed"]:
        msg = await bot.send_photo_if_exist(
            chat_id=message.from_user.id,
            caption=FSInputFile("images/already-gone.webp"),
            text="Опрос уже пройден",
            reply_markup=user_keyboard_main,
        )
        set_msg_id(message.from_user.id, msg.message_id)
        await bot.delete_message(message.from_user.id, message.message_id)
        return

    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=FSInputFile("images/are-u-ready.webp"),
        text=f"Готовы начать?",
        reply_markup=user_keyboard_survey_start,
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message(F.text.lower().in_({"задать вопрос 💬", "задать вопрос"}))
async def user_handler_question(message: Message, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")

    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=FSInputFile("images/ask-question.webp"),
        text=f"Кому хотите задать вопрос?",
        reply_markup=user_keyboard_ask_question,
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message(F.text.lower().in_({"спикеру 👔", "спикеру"}))
async def user_handler_ask_speaker(message: Message, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")

    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=FSInputFile("images/ask-speaker.webp"),
        text=f"Выберете спикера",
        reply_markup=user_keyboard_builder_speakers(),
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message(F.text.lower().in_({"администрации 🎩", "администрации"}))
async def user_handler_ask_management(message: Message, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")

    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=FSInputFile("images/ask-manager.webp"),
        text=f"Задайте любой интересующий вопрос",
        reply_markup=user_keyboard_builder_feedback(),
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message(User.question)
async def user_handler_confirm(message: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(question=message.text)

    userState = await state.get_data()
    speaker = get_by_id("speakers", userState["speaker_id"])
    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=speaker["img"],
        text=f"Подтвердите отправку вопроса для {speaker["name"]}:\n{message.text}",
        reply_markup=user_keyboard_confirm,
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)


@router.message()
async def error_message(message: Message, bot: Bot):
    await bot.delete_message(message.from_user.id, get_msg_id(message.from_user.id))
    await bot.send_chat_action(message.from_user.id, action="typing")

    msg = await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=FSInputFile("images/action-cancell.webp"),
        text=f"Что-то пошло не так...\nПопробуйте ввести /menu",
    )

    await bot.delete_message(message.from_user.id, message.message_id)
    set_msg_id(message.from_user.id, msg.message_id)

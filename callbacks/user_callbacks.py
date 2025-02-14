from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, URLInputFile
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from utils.states import User, Survey
from config.bot_config import IMG

router = Router()


@router.callback_query(F.data == "survey_start")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    await state.set_state(Survey.quizId)
    quiz = get_next_quiz()

    await state.update_data(quizId=quiz["id"])
    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=URLInputFile(quiz["img"]),
        text=f"{quiz["name"]}\n{quiz["content"]}",
        reply_markup=user_keyboard_builder_variants(quiz["id"]),
    )

    set_msg_id(callback.from_user.id, msg.message_id)


@router.callback_query(F.data == "survey_end")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    set_user_passed(callback.from_user.id)
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=URLInputFile(IMG),
        text="Результаты отправлены на доску",
        reply_markup=user_keyboard_main,
    )

    set_msg_id(callback.from_user.id, msg.message_id)
    await state.clear()


@router.callback_query(F.data.startswith("survey_answer"))
async def walkthrough_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    increment_variant(callback.data.partition("id=")[2])
    bot.google_table.updateSurvey(callback.data.partition("id=")[2])

    data = await state.get_data()
    quiz = get_next_quiz(data["quizId"])

    if quiz == None:
        msg = await bot.send_photo_if_exist(
            chat_id=callback.from_user.id,
            text="Поздравляем, ты ответил на все вопросы",
            caption=URLInputFile(IMG),
            reply_markup=user_keyboard_survey_end,
        )
    else:
        await state.update_data(quizId=quiz["id"])
        msg = await bot.send_photo_if_exist(
            chat_id=callback.from_user.id,
            caption=URLInputFile(quiz["img"]),
            text=f"{quiz["name"]}\n{quiz["content"]}",
            reply_markup=user_keyboard_builder_variants(quiz["id"]),
        )

    set_msg_id(callback.from_user.id, msg.message_id)


@router.callback_query(F.data.startswith("ask_speaker"))
async def ask_question_speaker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    await state.update_data(speaker_id=callback.data.partition("id=")[2])
    await state.set_state(User.question)
    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=URLInputFile(IMG),
        text=f"Введите вопрос:",
        reply_markup=user_keyboard_cancel,
    )

    set_msg_id(callback.from_user.id, msg.message_id)


@router.callback_query(F.data == "send_question")
async def send_question_speaker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    userState = await state.get_data()
    bot.google_table.setQuestion(userState["speaker_id"], userState["question"])
    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=URLInputFile(IMG),
        text=f"Ваш вопрос успешно доставлен",
        reply_markup=user_keyboard_main,
    )

    set_msg_id(callback.from_user.id, msg.message_id)
    await state.clear()


@router.callback_query(F.data == "none")
async def cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=URLInputFile(IMG),
        text=f"Действие отменено",
        reply_markup=user_keyboard_main,
    )

    set_msg_id(callback.from_user.id, msg.message_id)
    await state.clear()

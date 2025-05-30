from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from utils.states import User, Survey
from config.bot_config import IMG
from utils.parsers import *

router = Router()


@router.callback_query(F.data == "survey_start")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    await state.set_state(Survey.quizId)
    quiz = get_next_quiz()

    await state.update_data(quizId=quiz["id"])

    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=quiz["img"],
        text=f"{parse_quiz_content(quiz)}",
        reply_markup=user_keyboard_builder_variants(quiz["id"]),
    )

    set_msg_id(callback.from_user.id, msg.message_id)


@router.callback_query(F.data == "survey_end")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    set_user_passed(callback.from_user.id)
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=FSInputFile("images/result-sent.webp"),
        text="Результаты отправлены организаторам",
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
            text="Поздравляем, опрос пройден!",
            caption=FSInputFile("images/congratulate.webp"),
            reply_markup=user_keyboard_survey_end,
        )
    else:
        await state.update_data(quizId=quiz["id"])

        msg = await bot.send_photo_if_exist(
            chat_id=callback.from_user.id,
            caption=quiz["img"],
            text=f"{parse_quiz_content(quiz)}",
            reply_markup=user_keyboard_builder_variants(quiz["id"]),
        )

    set_msg_id(callback.from_user.id, msg.message_id)


@router.callback_query(F.data.startswith("ask_speaker"))
async def ask_question_speaker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.from_user.id, get_msg_id(callback.from_user.id))

    speaker = get_by_id(
        "speakers",
        callback.data.partition("id=")[2],
    )
    await state.update_data(speaker_id=speaker["id"])
    await state.set_state(User.question)
    msg = await bot.send_photo_if_exist(
        chat_id=callback.from_user.id,
        caption=speaker["img"],
        text=f"Введите вопрос для \n{speaker["name"]}, {speaker["content"]}",
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
        caption=FSInputFile("images/ask-sent.webp"),
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
        caption=FSInputFile("images/action-cancell.webp"),
        text=f"Действие отменено",
        reply_markup=user_keyboard_main,
    )

    set_msg_id(callback.from_user.id, msg.message_id)
    await state.clear()

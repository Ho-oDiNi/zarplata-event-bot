from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from utils.states import User, Survey

router = Router()


@router.callback_query(F.data == "survey_start")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    quiz = get_next_quiz()

    await state.set_state(Survey.quizId)
    await state.update_data(quizId=quiz["id"])
    await state.update_data(isChange={"0": 0})
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"{quiz["name"]}\n{quiz["content"]}",
        reply_markup=user_keyboard_builder_variants(quiz["id"]),
    )
    await callback.message.edit_reply_markup()


@router.callback_query(F.data == "survey_end")
async def start_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Результаты отправлены на доску",
        reply_markup=user_keyboard_main,
    )
    await callback.message.edit_reply_markup()


@router.callback_query(F.data.startswith("survey_answer"))
async def walkthrough_survey(callback: CallbackQuery, state: FSMContext, bot: Bot):
    increment_variant(callback.data.partition("id=")[2])
    bot.google_table.updateSurvey(callback.data.partition("id=")[2])

    data = await state.get_data()
    quiz = get_next_quiz(data["quizId"])

    if quiz == None:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text="Поздравляем, ты ответил на все вопросы",
            reply_markup=user_keyboard_survey_end,
        )
    else:
        await state.update_data(quizId=quiz["id"])
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"{quiz["name"]}\n{quiz["content"]}",
            reply_markup=user_keyboard_builder_variants(quiz["id"]),
        )

    await callback.message.edit_reply_markup()


@router.callback_query(F.data.startswith("ask_speaker"))
async def ask_question_speaker(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speaker_id=callback.data.partition("id=")[2])
    await state.set_state(User.question)
    await callback.message.answer(
        text=f"Введите вопрос:", reply_markup=user_keyboard_main
    )


@router.callback_query(F.data == "send_question")
async def send_question_speaker(callback: CallbackQuery, state: FSMContext, bot: Bot):
    userState = await state.get_data()
    bot.google_table.setQuestion(userState["speaker_id"], userState["question"])
    await callback.answer(text=f"Ваш вопрос успешно доставлен")
    await callback.message.edit_reply_markup()
    await state.clear()


@router.callback_query(F.data == "none")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"Действие отменено")
    await callback.message.edit_reply_markup()
    await state.clear()

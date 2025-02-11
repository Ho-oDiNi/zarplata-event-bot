from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.user_reply_keyboards import *
from keyboards.user_inline_keyboards import *
from utils.db_requests import *
from utils.states import User

router = Router()


@router.callback_query(F.data == "start_quiz")
async def walkthrough_quiz(callback: CallbackQuery):
    await callback.answer(text=f"В разработке")


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

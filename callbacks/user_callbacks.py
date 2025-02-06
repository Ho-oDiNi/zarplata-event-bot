from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from filters.isUserFilter import IsUserFilter
from keyboards.user_ReplyKeyboards import *
from keyboards.user_InlineKeyboards import *
from utils.requests import *
from utils.states import User

router = Router()
router.message.filter(IsUserFilter())


@router.callback_query(F.data == "start_survey")
async def walkthrough_survey(callback: CallbackQuery):
    await callback.answer(text=f"В разработке")


@router.callback_query(F.data.startswith("ask_speaker"))
async def send_question_speaker(callback: CallbackQuery, state: FSMContext):
    speaker_name = get_field_by_id("speakers", callback.data.partition("id=")[2])[
        "name"
    ]
    await state.update_data(speaker=speaker_name)
    await state.set_state(User.question)
    await callback.message.answer(
        text=f"Введите вопрос:", reply_markup=user_keyboard_main
    )


@router.callback_query(F.data == "none")
async def cancel_log(callback: CallbackQuery):
    await callback.answer(text=f"Действие отменено")
    await callback.message.edit_reply_markup()

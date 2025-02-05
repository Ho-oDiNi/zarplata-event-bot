from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from filters.isUserFilter import IsUserFilter
from keyboards.user_ReplyKeyboards import *
from keyboards.user_InlineKeyboards import *
from utils.requests import *

router = Router()
router.message.filter(IsUserFilter())


@router.callback_query(F.data == "start_survey")
async def walkthrough_survey(callback: CallbackQuery, bot: Bot):
    await callback.answer(text=f"В разработке")


@router.callback_query(F.data.startswith("ask_speaker"))
async def send_question_speaker(callback: CallbackQuery, bot: Bot):
    speaker_id = callback.data.partition("id=")[2]
    await callback.message.answer(text=f"Введите вопрос:")


@router.callback_query(F.data == "none")
async def cancel_log(callback: CallbackQuery):
    await callback.answer(text=f"Действие отменено")
    await callback.message.edit_reply_markup()

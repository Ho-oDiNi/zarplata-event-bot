from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.isAdminFilter import IsAdminFilter
from keyboards.admin_InlineKeyboards import *

router = Router()
router.message.filter(IsAdminFilter())


@router.callback_query(F.data == "None")
async def cancel_log(callback: CallbackQuery):
    await callback.answer(text=f"Действие отклонено")
    await callback.message.edit_reply_markup()

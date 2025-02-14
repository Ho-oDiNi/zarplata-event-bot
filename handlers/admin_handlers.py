from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.admin_reply_keyboards import *
from keyboards.admin_inline_keyboards import *
from filters.admin_filter import IsAdminFilter
from aiogram.fsm.context import FSMContext
from utils.states import *

router = Router()
router.message.filter(IsAdminFilter())


@router.message(F.text.lower().in_({"в главное меню", "меню"}))
@router.message(Command("menu", "start"))
async def admin_handler_menu(message: Message, state: FSMContext):
    await message.answer(text=f"Выберите действие:", reply_markup=admin_keyboard_main)


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

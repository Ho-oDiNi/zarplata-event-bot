from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.admin_ReplyKeyboards import *
from filters.isAdminFilter import IsAdminFilter

router = Router()
router.message.filter(IsAdminFilter())


@router.message(F.text.lower().in_({"назад", "меню"}))
@router.message(Command("menu", "start"))
async def admin_handler_menu(message: Message):
    await message.answer(text=f"Выберите действие:", reply_markup=admin_keyboard_main)


@router.message(F.text.lower() == "настройки конференции")
async def admin_handler_setting(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=admin_keyboard_settings)


@router.message(F.text.lower() == "изменить название")
async def admin_handler_change_title(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=admin_keyboard_in_develop)


@router.message(F.text.lower() == "ввести опрос")
async def admin_handler_change_survey(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=admin_keyboard_in_develop)


@router.message(F.text.lower() == "ввести данные о спикерах")
async def admin_handler_change_speakers(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=admin_keyboard_in_develop)


@router.message(F.text.lower() == "отправить рассылку")
async def admin_handler_send_mailing(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=admin_keyboard_in_develop)


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

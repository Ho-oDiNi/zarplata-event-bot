from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.moderator_ReplyKeyboards import *
from filters.isModeratorFilter import IsModeratorFilter

router = Router()
router.message.filter(IsModeratorFilter())


@router.message(F.text.lower().in_({"назад", "меню"}))
@router.message(Command("menu", "start"))
async def admin_handler_menu(message: Message):
    await message.answer(
        text=f"Выберите действие:", reply_markup=moderator_keyboard_main
    )


@router.message(F.text.lower() == "начать конференцию")
async def admin_handler_start(message: Message):
    await message.answer(
        text=f"В РАЗРАБОТКЕ", reply_markup=moderator_keyboard_conference
    )


@router.message(F.text.lower() == "перейти к следующему спикеру")
async def admin_handler_next_speaker(message: Message):
    await message.answer(
        text=f"В РАЗРАБОТКЕ", reply_markup=moderator_keyboard_in_develop
    )


@router.message(F.text.lower() == "завершить конференцию")
async def admin_handler_stop(message: Message):
    await message.answer(text=f"В РАЗРАБОТКЕ", reply_markup=moderator_keyboard_main)


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

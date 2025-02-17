from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.admin_reply_keyboards import *
from keyboards.admin_inline_keyboards import *
from filters.admin_filter import IsAdminFilter
from aiogram.fsm.context import FSMContext
from utils.states import Admin

router = Router()
router.message.filter(IsAdminFilter())


@router.message(F.text.lower().in_({"в главное меню", "меню"}))
@router.message(Command("menu", "start"))
async def admin_handler_menu(message: Message):
    await message.answer(text=f"Выберите действие:", reply_markup=admin_keyboard_main)


@router.message(Admin.massMailing)
async def admin_handler_mailing(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(massMailing=message.text)

    adminState = await state.get_data()
    event = get_by_id("events", adminState["requestId"])
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Подтвердите отправку вопроса для всех юзеров {event["name"]}:\n{message.text}",
        reply_markup=admin_keyboard_confirm("send_mailing"),
    )


@router.message(Admin.changeField)
async def admin_handler_mailing(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(changeField=message.text)

    adminState = await state.get_data()
    data = get_by_id(adminState["requestTable"], adminState["requestId"])
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Подтвердите изменение c {data[adminState["requestField"]]} на {message.text}",
        reply_markup=admin_keyboard_confirm("change_field"),
    )


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

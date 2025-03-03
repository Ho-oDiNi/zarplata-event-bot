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
    await message.answer(text=f"Выберите действие:", reply_markup=admin_keyboard_main())


@router.message(Admin.massMailing)
async def admin_handler_mailing(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(massMailing=message.text)
    await state.update_data(addPhoto=None)

    await state.set_state(Admin.addPhoto)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Прикрепите изображение для отправки\nИЛИ нажмите 'Подтвердить' для отправки",
        reply_markup=admin_keyboard_confirm("send_mailing"),
    )


@router.message(Admin.addPhoto)
async def add_photo_mailing(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(addPhoto=message.photo[-1].file_id)
    adminState = await state.get_data()

    event = get_by_id("events", adminState["requestId"])
    await bot.send_photo_if_exist(
        chat_id=message.from_user.id,
        caption=adminState["addPhoto"],
        text=f"Подтвердите отправку вопроса для {event["name"]}:\n{adminState["massMailing"]}",
        reply_markup=admin_keyboard_confirm("send_mailing"),
    )


@router.message(Admin.changeRow)
async def admin_handler_changing(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(changeRow=message.text)

    adminState = await state.get_data()
    data = get_by_id(adminState["requestTable"], adminState["requestId"])
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Подтвердите изменение c {data[adminState["requestField"]]}\n{message.text}",
        reply_markup=admin_keyboard_confirm("change_row"),
    )


@router.message(Admin.createRow)
async def admin_handler_creating(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    await state.update_data(createRow=message.text)

    adminState = await state.get_data()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Подтвердите создание поля {adminState["requestTable"]}\n{message.text}",
        reply_markup=admin_keyboard_confirm("create_row"),
    )

@router.message(Admin.changeFileId)
async def admin_handler_changing_img(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id
    
    await state.update_data(changeFileId=file_id)
    adminState = await state.get_data()
    update_by_id(
        adminState["requestTable"],
        adminState["requestField"],
        adminState["requestId"],
        adminState["changeFileId"],
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Успешно изменено",
        reply_markup=admin_keyboard_main(),
    )
    await state.clear()


@router.message()
async def echo(message: Message):
    await message.answer(text=f"Что-то пошло не так...\nПопробуйте ввести /menu")

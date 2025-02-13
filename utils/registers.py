from aiogram import Bot
from config.bot_config import ADMIN, DB


async def send_photo_register(bot: Bot, tg_id, img, message, keyboard):
    try:
        await bot.send_photo(
            chat_id=tg_id,
            photo=img,
            caption=message,
            reply_markup=keyboard,
        )
    except:
        await bot.send_message(
            chat_id=tg_id,
            text=message,
            reply_markup=keyboard,
        )


async def start_bot_register(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот перезапущен")


async def stop_bot_register(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот отключился")
    DB.close()

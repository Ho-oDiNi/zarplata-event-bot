from aiogram import Bot
from config.bot_config import ADMIN, DB


async def send_photo_register(bot: Bot, tg_id, img, user_message, keyboard):
    try:
        msg = await bot.send_photo(
            chat_id=tg_id,
            photo=img,
            caption=user_message,
            reply_markup=keyboard,
        )
    except:
        msg = await bot.send_message(
            chat_id=tg_id,
            text=user_message,
            reply_markup=keyboard,
        )
    finally:
        return msg


async def send_file_register(bot: Bot, tg_id, doc, user_message, keyboard):
    try:
        msg = await bot.send_document(
            chat_id=tg_id,
            document=doc,
            caption=user_message,
            reply_markup=keyboard,
        )
    except:
        msg = await bot.send_message(
            chat_id=tg_id,
            text=user_message,
            reply_markup=keyboard,
        )
    finally:
        return msg


async def start_bot_register(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот перезапущен")


async def stop_bot_register(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот отключился")
    DB.close()

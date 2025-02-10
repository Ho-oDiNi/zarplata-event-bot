from aiogram import Bot
from config.bot_config import ADMIN, DB


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот перезапущен")


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот отключился")
    DB.close()

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.bot_config import GOOGLE_URL, API_TOKEN
from api_google.google_table import GoogleTable
from utils.registers import *
from callbacks import *
from handlers import *


async def main():
    logging.basicConfig(level=logging.INFO)

    class ZPEventBot(Bot):
        def __init__(self, token, google_table=None):
            super().__init__(token)
            self.google_table: GoogleTable = google_table

        async def send_photo_if_exist(self, chat_id, caption, text, reply_markup=None):
            return await send_photo_register(self, chat_id, caption, text, reply_markup)

    bot: ZPEventBot = ZPEventBot(
        token=API_TOKEN,
        google_table=GoogleTable("config/google_config.json", GOOGLE_URL),
    )
    dp = Dispatcher()

    dp.startup.register(start_bot_register)
    dp.shutdown.register(stop_bot_register)

    dp.include_routers(
        admin_handlers.router,
        admin_callbacks.router,
        user_handlers.router,
        user_callbacks.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

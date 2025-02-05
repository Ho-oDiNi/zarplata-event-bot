import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.bot_config import GOOGLE_URL, API_TOKEN, ADMIN, DB
from callbacks import *
from handlers import *
from api_google.google_table import GoogleTable


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Бот перезапущен")


async def stop_bot(bot: Bot):
    DB.close()
    await bot.send_message(chat_id=ADMIN, text="Бот отключился")


async def main():
    logging.basicConfig(level=logging.INFO)

    class LodgerPlusBot(Bot):
        def __init__(self, token, google_table=None):
            super().__init__(token)
            self.google_table: GoogleTable = google_table

    bot: LodgerPlusBot = LodgerPlusBot(
        token=API_TOKEN,
        google_table=GoogleTable("config/google_config.json", GOOGLE_URL),
    )
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        admin_handlers.router,
        moderator_handlers.router,
        # moderators_callbacks.router,
        user_handlers.router,
        user_callbacks.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

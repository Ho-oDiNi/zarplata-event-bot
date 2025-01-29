#Импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.bot_config import GOOGLE_URL, API_TOKEN
from callbacks import admin_callbacks
from handlers import admin_handlers, new_user_handlers, user_handlers
from handlers.new_user_handlers import router
from handlers.user_handlers import router
from handlers.admin_handlers import router
from callbacks.admin_callbacks import router
from google_table.google_table import GoogleTable


async def start_bot(bot: Bot):
    admins_id = db_get_admins()
    for admin_id in admins_id:
        await bot.send_message(chat_id = admin_id, text = "Бот перезапущен")

async def stop_bot(bot: Bot):
    admins_id = db_get_admins()
    for admin_id in admins_id:
        await bot.send_message(chat_id = admin_id, text = "Бот отключился")

async def main():
    logging.basicConfig(level=logging.INFO)

    #Запуск бота и диспатчера
    class LodgerPlusBot(Bot):
        def __init__(
                self,
                token,
                google_table = None
        ):
            super().__init__(token)
            self.google_table : GoogleTable = google_table

    bot: LodgerPlusBot = LodgerPlusBot(
        token = API_TOKEN,
        google_table = GoogleTable("config/google_config.json", GOOGLE_URL),

    )
    dp = Dispatcher()
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        admin_handlers.router,
        admin_callbacks.router,
        speaker_handlers.router,
        user_handlers.router,
        user_callbacks.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 


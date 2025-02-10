from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.requests import *


# Кэшируется запрос к БД?
class HasEventFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if get_current_event() == None:
            await message.answer("Извини, но сегодня нет активных ивентов :(")
            return False

        return True

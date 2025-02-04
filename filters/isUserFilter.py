from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.requests import *


class IsUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        users_id = get_array_id(db_get_table("users"))
        if message.from_user.id in users_id:
            return True

        return False

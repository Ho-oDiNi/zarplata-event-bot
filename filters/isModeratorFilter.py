from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.requests import *


class IsModeratorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        moderators_id = get_array_id(db_get_table("moderators"))
        if message.from_user.id in moderators_id:
            return True

        return False

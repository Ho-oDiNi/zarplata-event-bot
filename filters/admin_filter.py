from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.bot_config import ADMIN, MANAGER


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in [ADMIN, MANAGER]:
            return True

        return False

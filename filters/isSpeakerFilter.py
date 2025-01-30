from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsSpeakerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        speakers_id = db_get_users()
        if message.from_user.id in speakers_id:
            return True

        return False

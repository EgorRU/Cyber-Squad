from aiogram.filters import BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from db import is_admin


class FilterAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return await is_admin(message.from_user.id)
    

class GetAdminId(StatesGroup):
    id_user = State()
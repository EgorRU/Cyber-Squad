from aiogram.filters import BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from db import is_admin


#фильтрация для админа
class FilterAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return await is_admin(message.from_user.id, message.from_user.username)
    

#Машина состояний для получения username пользователя
class GetAdminId(StatesGroup):
    id_user = State()
   
    
#машина состояний для получения обновлённой ссылки
class GetNewUrl(StatesGroup):
    new_url = State()
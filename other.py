from aiogram.types import Message
from aiogram import Router
from my_filter import FilterAdmin
from db import update_db, set_new_url, mailing


other = Router()


#ловим сообщения со ссылкой от админов
@other.message(FilterAdmin())
async def start(message: Message):
    await set_new_url(message.text)
    await message.answer(f"Ваша ссылка:\n{message.text}\nПринята в работу")
    await mailing()
    

#пользователям отвечаем, что они не могут писать
@other.message()
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer("Недостаточно прав, Вы не администратор")
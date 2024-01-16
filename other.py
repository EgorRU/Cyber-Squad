import sqlite3
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import BaseFilter
from db import is_admin, set_new_url, update_db, mailing


other = Router()


#фильтрация для админа
class FilterAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return await is_admin(message.from_user.id)
   

#ловим сообщения со ссылкой от админа
@other.message(FilterAdmin())
async def start(message: Message):
    #если успешно добавили ссылку, то делаем рассылку
    if await set_new_url(message.text):
        await mailing() #рассылка
        await message.answer(f"Ваша ссылка:\n{message.text}\nПринята в работу")
    else:
        await message.answer(f"Ваша ссылка:\n{message.text}\n❗❗НЕ принята в работу") #повторка
    

#для всех остальных отправляем, что они не могут ничего отправлять 
@other.message()
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer("Вы не можете отправлять ссылки")
    

#создание бд
async def create_db():
    base = sqlite3.connect("database.db")
    base.execute("CREATE TABLE IF NOT EXISTS users(id_user integer PRIMARY KEY, fullname TEXT, username TEXT, count_ready_url integer, is_admin integer)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS urls(urlname TEXT PRIMARY KEY, url TEXT, count_ready integer)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS users_urls(id_user integer, urlname TEXT, is_ready integer, PRIMARY KEY(id_user, urlname))")
    base.commit()
    base.close()
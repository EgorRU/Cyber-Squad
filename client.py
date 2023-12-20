from aiogram import Router, F
from aiogram.types import Message
from db import update_db, is_admin
from other import get_keyboard_and_message_text


client = Router()


@client.message(F.text == '/start')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        await message.answer("❗Вы администратор\nДля рассылки нового сообщения отправьте сообщение боту\n\n❗/info  - вывести текущую ситуацию по ссылкам\n❗/admin  - вывести панель управления")
    else:
        await message.answer("Ожидайте сообщений от бота. Актуальную информацию по необработанным ссылкам можно посмотреть по команде /info")


@client.message(F.text == '/info')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    keyboard, message_text = await get_keyboard_and_message_text()
    await message.answer(message_text, reply_markup=keyboard, disable_web_page_preview=True)
    

@client.message(F.text == '/help')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        await message.answer("❗/admin - вызвать панель управления\n❗/addadmin <id> - добавить человека по id в администраторы\n❗/removeadmin <id> - удалить человека по id из администраторов\n❗/deleteurl <url> - удалить ссылку из таблицы по её url-адресу\n❗/info - вывести текущую ситуацию по ссылкам\n\n\n❓Как получить id человека в tg?\n\n✅Переслать любое сообщение от человека, которого хотите добавить в админы, этому боту @getmyid_bot\nНужный id будет в строке 'Forwarded from'")
    else:
        await message.answer("❗/info  - вывести текущую ситуацию по ссылкам")
  

from aiogram import Router, F
from aiogram.types import Message
from db import update_db, is_admin, get_keyboard_and_message_text


client = Router()

@client.message(F.text == '/start')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id, message.from_user.username):
        await message.answer("❗Вы администратор\nДля рассылки нового сообщения отправьте сообщение боту\n\n❗/info  - вывести текущую ситуацию по ссылкам\n❗/admin  - вывести панель управления\n")
    else:
        await message.answer("Ожидайте сообщений от бота. Актуальную информацию по необработанным ссылкам можно посмотреть по команде /info")


@client.message(F.text == '/info')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    keyboard, message_text = await get_keyboard_and_message_text("show")
    await message.answer(message_text, reply_markup=keyboard, disable_web_page_preview=True)
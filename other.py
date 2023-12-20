from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram import Router
from db import get_url, get_all_id_user, update_db, update_url
from config import bot


other = Router()


async def get_keyboard_and_message_text():
    list_url = await get_url()
    if len(list_url) > 0:
        if len(list_url)>50:
            list_url = list_url[-50:]
        text_message = ""
        index = 1
        inner_keyboard = []
        inline_keyboard = []
        for tuple_url in list_url:
            link = tuple_url[0]
            string = "❌" if tuple_url[1]==0 else "✅"
            text_message += f"{index}) {link} {string}\n"
            inner_keyboard.append(InlineKeyboardButton(text=f'{index}{string}', callback_data=f'{link if len(link)<64 else link[-64:]}'))
            index += 1
            if len(inner_keyboard)>4:
                inline_keyboard.append(inner_keyboard)
                inner_keyboard = []
        else:
            inline_keyboard.append(inner_keyboard)
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return keyboard, text_message
    else:
        return None, "Нет необработанных ссылок"
    

async def mailing():
    all_id_user = await get_all_id_user()
    keyboard, text_message = await get_keyboard_and_message_text()
    for id_user in all_id_user:
        try:
            await bot.send_message(id_user, f"Появились новые ссылки:\n{text_message}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
        

@other.message()
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer("Недостаточно прав")
    

@other.callback_query()
async def start(callback: CallbackQuery):
    await update_url(callback.data)
    keyboard, message_text = await get_keyboard_and_message_text()
    try:
        await callback.message.edit_text(f"Обновлённый список ссылок:\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
    except:
        pass
    await callback.answer()
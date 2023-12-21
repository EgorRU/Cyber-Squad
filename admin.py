from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from my_filter import  GetAdminId, GetNewUrl
from db import is_admin, update_db, get_admin
from db import delete_url, update_url, swap_status_url, edit_url
from db import add_admin, delete_admin
from db import get_keyboard_and_message_text


admin = Router()
    

@admin.message(F.text == '/admin')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id, message.from_user.username):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Управление администраторами', callback_data='Управление администраторами')],
        [InlineKeyboardButton(text='Редактирование таблицы', callback_data='Редактирование таблицы')],
        ])
        await message.answer("Панель управления", reply_markup=keyboard)
    else:
        await message.answer("Недостаточно прав")
    

#получение username для назвачения нового админа
@admin.message(GetAdminId.id_user)
async def start(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id, message.from_user.username):
        try:
            username = message.text
            if username[0]=="@":
                username = username[1:]
            await add_admin(username)
            keyboard, text = await get_admin()
            await message.answer(f"Успешно\n{text}", reply_markup=keyboard)
            await state.clear()
        except:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Отмена')]])
            await message.answer("Неверный формат, попробуйте ещё раз или ❗нажмите отмена", reply_markup=keyboard)
    else:
        await message.answer("❗Вы больше не администратор")
    

#получение нового url для изменения
@admin.message(GetNewUrl.new_url)
async def start(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id, message.from_user.username):
        new_url = message.text
        data = await state.get_data()
        old_url = data["callback"]
        await state.clear()
        await edit_url(old_url, new_url)
        keyboard, message_text = await get_keyboard_and_message_text("edit")
        try:
            await message.answer(f"❓Какие ссылки вы хотите отредактировать?\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        await message.answer("❗Вы больше не администратор")


@admin.callback_query(F.data == 'Управление администраторами')
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, text = await get_admin()
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(F.data == 'Редактирование таблицы')
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Удаление ссылок', callback_data='Удаление ссылок')],
        [InlineKeyboardButton(text='Редактирование ссылок', callback_data='Редактирование ссылок')],
        [InlineKeyboardButton(text="Смена статуса с 'yes' на 'no' и наоборот", callback_data="Смена статуса с 'yes' на 'no'")],
        [InlineKeyboardButton(text='Назад', callback_data='Назад')],
        ])
        await callback.message.edit_text("Панель управления", reply_markup=keyboard)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(F.data == 'Назад')
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Управление администраторами', callback_data='Управление администраторами')],
        [InlineKeyboardButton(text='Редактирование таблицы', callback_data='Редактирование таблицы')],
        ])
        await callback.message.edit_text("Панель управления", reply_markup=keyboard)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(StateFilter(None), F.data == 'Добавить админа')
async def start(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Отмена')]])
        await callback.message.edit_text("❗Напишите @username пользователя для добавления", reply_markup=keyboard)
        await state.set_state(GetAdminId.id_user)
        await callback.answer("Если вы не собираетесь добавлять администратора, то нажмите обязательно на кнопку 'отмена'", show_alert=True)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(F.data == 'Удаление ссылок')
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, message_text = await get_keyboard_and_message_text("dele")
        try:
            await callback.message.edit_text(f"❓Какие ссылки вы хотите удалить?\n\n❗Нажатие на кнопку - удаление без подтверждения\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(F.data == 'Редактирование ссылок')
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, message_text = await get_keyboard_and_message_text("edit")
        try:
            await callback.message.edit_text(f"❓Какие ссылки вы хотите отредактировать?\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(F.data == "Смена статуса с 'yes' на 'no'")
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, message_text = await get_keyboard_and_message_text("swap")
        try:
            await callback.message.edit_text(f"❓У какой ссылки вы хотите изменить статус?\n\n❗Нажатие на кнопку - изменение статуса без подтверждения\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

#нажата кнопка - удалить админа, его id(username) в callback
@admin.callback_query(F.data.startswith("deleteadmin"))
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        await delete_admin((callback.data[11:]))
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, text = await get_admin()
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

@admin.callback_query(GetAdminId.id_user, F.data == 'Отмена')
async def start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        keyboard, text = await get_admin()
        await callback.message.edit_text(text, reply_markup=keyboard)
    except:
        pass
    await callback.answer()
  
    
@admin.callback_query(GetNewUrl.new_url, F.data == 'Отмена')
async def start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard, message_text = await get_keyboard_and_message_text("edit")
        try:
            await callback.message.edit_text(f"❓Какие ссылки вы хотите отредактировать?\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
    

#нажата кнопка, чтобы поменять статус ссылки на заблокированный(для всех)
@admin.callback_query(F.data.startswith("show"))
async def start(callback: CallbackQuery):
    await update_url(callback.data[4:])
    keyboard, message_text = await get_keyboard_and_message_text("show")
    try:
        await callback.message.edit_text(f"Обновлённый список ссылок:\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
    except:
        pass
    await callback.answer()
     
    
#нажата кнопка, чтобы изменить ссылку
@admin.callback_query(StateFilter(None), F.data.startswith("edit"))
async def start(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Отмена')]])
        await callback.message.edit_text(f"Старая ссылка: {callback.data[4:]}\nНапишите новую ссылку", reply_markup=keyboard)
        await state.set_data({"callback" : f"{callback.data[4:]}"})
        await state.set_state(GetNewUrl.new_url)
        await callback.answer("Если вы не собираетесь изменять ссылку, то нажмите обязательно на кнопку 'отмена'", show_alert=True)
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
       
        
#нажата кнопка, чтобы удалить ссылку
@admin.callback_query(F.data.startswith("dele"))
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        await delete_url(callback.data[4:])
        keyboard, message_text = await get_keyboard_and_message_text("dele")
        try:
            await callback.message.edit_text(f"❓Какие ссылки вы хотите удалить?\n\n❗Нажатие на кнопку - удаление без подтверждения\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
        

#нажата кнопка, чтобы поменять статус ссылки
@admin.callback_query(F.data.startswith("swap"))
async def start(callback: CallbackQuery):
    if await is_admin(callback.from_user.id, callback.from_user.username):
        await swap_status_url(callback.data[4:])
        keyboard, message_text = await get_keyboard_and_message_text("swap")
        try:
            await callback.message.edit_text(f"❓У какой ссылки вы хотите изменить статус?\n\n❗Нажатие на кнопку - изменение статуса без подтверждения\n\n{message_text}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
    else:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer("❗Вы больше не администратор")
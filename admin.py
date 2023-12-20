from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from my_filter import FilterAdmin, GetAdminId
from db import is_admin, update_db, get_admin
from db import set_new_url, delete_url
from db import add_admin, delete_admin
from other import mailing


admin = Router()
    

@admin.message(F.text == '/admin')
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Управление администраторами', callback_data='Управление администраторами')],
        [InlineKeyboardButton(text='Редактирование таблицы', callback_data='Редактирование таблицы')],
        ])
        await message.answer("Панель управления", reply_markup=keyboard)
    else:
        await message.answer("Недостаточно прав")
    
    
@admin.message(F.text.startswith("/addadmin"))
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        if len(message.text[10:])>0:
            if await add_admin(int(message.text[10:])):
                await message.answer("Успешно добавлен админ")
            else:
                await message.answer("Не удалось добавить")
    else:
        await message.answer("Недостаточно прав")
        

@admin.message(F.text.startswith("/deleteurl"))
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        if len(message.text[11:])>0:
            if await delete_url(message.text[11:]):
                await message.answer("Успешно удалена ссылка")
            else:
                await message.answer("Не удалось удалить")
    else:
        await message.answer("Недостаточно прав")
        

@admin.message(F.text.startswith("/removeadmin"))
async def start(message: Message):
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if await is_admin(message.from_user.id):
        if len(message.text[13:])>0:
           if await delete_admin(int(message.text[13:])):
               await message.answer("Успешно удалён админ")
           else:
               await message.answer("Такого админа нет")
    else:
        await message.answer("Недостаточно прав")
        

@admin.message(FilterAdmin())
async def start(message: Message):
    await set_new_url(message.text)
    await message.answer(f"Ваша ссылка:\n{message.text}\nПринята в работу")
    await mailing()
    

@admin.message(GetAdminId.id_user)
async def start(message: Message, state: FSMContext):
    try:
        message_array = message.text.split()
        id_user, name_user = int(message_array[0]), message_array[1]
        await update_db(id_user, name_user, None)
        await add_admin(id_user)
        await state.clear()
        keyboard, text = await get_admin()
        await message.answer(f"Успешно\n{text}", reply_markup=keyboard)
    except:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Отмена')]])
        await message.answer("Неверный формат, попробуйте ещё раз или ❗нажмите отмена", reply_markup=keyboard)
    


    





        

@admin.callback_query(F.data == 'Управление администраторами')
async def start(callback: CallbackQuery):
    keyboard, text = await get_admin()
    await callback.message.edit_text(text, reply_markup=keyboard)
    

@admin.callback_query(F.data == 'Редактирование таблицы')
async def start(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удаление ссылок', callback_data='Удаление ссылок')],
    [InlineKeyboardButton(text='Редактирование ссылок', callback_data='Редактирование ссылок')],
    [InlineKeyboardButton(text="Смена статуса с 'yes' на 'no'", callback_data="Смена статуса с 'yes' на 'no'")],
    [InlineKeyboardButton(text='Назад', callback_data='Назад')],
    ])
    await callback.message.edit_text("Панель управления", reply_markup=keyboard)
    

@admin.callback_query(F.data == 'Назад')
async def start(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Управление администраторами', callback_data='Управление администраторами')],
    [InlineKeyboardButton(text='Редактирование таблицы', callback_data='Редактирование таблицы')],
    ])
    await callback.message.edit_text("Панель управления", reply_markup=keyboard)
    

@admin.callback_query(StateFilter(None), F.data == 'Добавить админа')
async def start(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='Отмена')]])
    await callback.message.edit_text("Напишите id и имя пользователя одним сообщением\n\n❗Например, 234234234 Иван", reply_markup=keyboard)
    await state.set_state(GetAdminId.id_user)
    await callback.answer("Если вы не собираетесь добавлять администратора, то нажмите обязательно на кнопку 'отмена'", show_alert=True)
    

@admin.callback_query(F.data == 'Удаление ссылок')
async def start(callback: CallbackQuery):
    await callback.answer("В разработке", show_alert=True)
    

@admin.callback_query(F.data == 'Редактирование ссылок')
async def start(callback: CallbackQuery):
    await callback.answer("В разработке", show_alert=True)
    

@admin.callback_query(F.data == "Смена статуса с 'yes' на 'no'")
async def start(callback: CallbackQuery):
    await callback.answer("В разработке", show_alert=True)
    

@admin.callback_query(F.data.startswith("admin"))
async def start(callback: CallbackQuery):
    await delete_admin(int(callback.data[5:]))
    keyboard, text = await get_admin()
    await callback.message.edit_text(text, reply_markup=keyboard)
    

@admin.callback_query(GetAdminId.id_user, F.data == 'Отмена')
async def start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        keyboard, text = await get_admin()
        await callback.message.edit_text(text, reply_markup=keyboard)
    except:
        pass
    await callback.answer()
    


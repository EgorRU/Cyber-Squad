from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Router, F
from db import update_db
from db import get_count_not_ready_urls_for_user
from db import get_count_ready_urls_for_user
from db import get_list_urls_in_work_for_user
from db import get_list_ready_urls_for_user
from db import get_url_by_urlname
from db import report_by_link


client = Router()


#/start
@client.message(F.text == '/start')
async def start(message: Message):
    #обновляем данные пользователя
    await update_db(message.from_user.id, message.from_user.full_name, message.from_user.username)
    #получаем сколько ссылок сделано и сколько не сделано конкретным пользователем
    count_not_ready_urls = await get_count_not_ready_urls_for_user(message.from_user.id)
    count_ready_urls = await get_count_ready_urls_for_user(message.from_user.id)
    #создаём кнопки для клавы
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text=f'⚡Новые задания({count_not_ready_urls})', callback_data='Ссылки в работе-0')])
    inline_keyboard.append([InlineKeyboardButton(text=f'✔Выполнено({count_ready_urls})', callback_data='Выполнено')])
    #собираем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await message.answer("Добро пожаловать!", reply_markup=keyboard)
    

#Возврат в меню
@client.callback_query(F.data == "Меню")
async def menu(callback: CallbackQuery):
    #получаем сколько ссылок сделано и сколько не сделано конкретным пользователем
    count_not_ready_urls = await get_count_not_ready_urls_for_user(callback.from_user.id)
    count_ready_urls = await get_count_ready_urls_for_user(callback.from_user.id)
    #создаём кнопки для клавы
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text=f'⚡Новые задания({count_not_ready_urls})', callback_data='Ссылки в работе-0')])
    inline_keyboard.append([InlineKeyboardButton(text=f'✔Выполнено({count_ready_urls})', callback_data='Выполнено')])
    #собираем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await callback.message.edit_text("Добро пожаловать!", reply_markup=keyboard)


#ССЫЛКИ В РАБОТЕ-
@client.callback_query(F.data.startswith("Ссылки в работе-"))
async def urls_in_work(callback: CallbackQuery):
    #обновляем данные пользователя
    await update_db(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
    #получаем ссылки в работе
    list_urls_in_work = await get_list_urls_in_work_for_user(callback.from_user.id)
    count_urls_in_list = 10 #на каждом листе по count_urls_in_list ссылок
    #sheet - номер листа
    message_text = callback.data
    index = message_text.find("-")
    sheet = int(message_text[index+1:])
    #формируем кнопки и текст для отправки одного сообщения
    #если ссылки есть
    if len(list_urls_in_work) > 0:
        #отображаем ссылки, которые находятся в работе на конкретном листе
        index_start = sheet * count_urls_in_list
        index_end = index_start + count_urls_in_list - 1
        #если на последнем листе меньше, чем влазит всего
        if len(list_urls_in_work)-1 < index_end:
            index_end = len(list_urls_in_work) - 1
        #текст для отправки
        message_text = f"Лист №{sheet+1}"
        #создаём кнопки для клавы
        inline_keyboard = []
        for index in range(index_start, index_end+1):
            inline_keyboard.append([InlineKeyboardButton(text=f'#{index+1} | {list_urls_in_work[index]}', callback_data=f'url:{list_urls_in_work[index]}')])
        #кнопки - назад и вперёд - временный массив
        inline_keyboard_for_movement = []
        if sheet>0:
            inline_keyboard_for_movement.append(InlineKeyboardButton(text='Пред. страница', callback_data=f'Ссылки в работе-{sheet-1}'))
        if len(list_urls_in_work)-1 > index_end:
            inline_keyboard_for_movement.append(InlineKeyboardButton(text='След. страница', callback_data=f'Ссылки в работе-{sheet+1}'))
        #создаём кнопки назад и вперёд в общую массив кнопок
        inline_keyboard.append(inline_keyboard_for_movement)
        #добавляем кнопку назад
        inline_keyboard.append([InlineKeyboardButton(text="Меню", callback_data='Меню')])
    #если рабочих ссылок нет
    else:
        message_text = '❗️Нет рабочих ссылок'
        #создаём кнопки для клавы
        inline_keyboard = []
        count_not_ready_urls = await get_count_not_ready_urls_for_user(callback.from_user.id)
        count_ready_urls = await get_count_ready_urls_for_user(callback.from_user.id)
        inline_keyboard.append([InlineKeyboardButton(text=f'⚡Новые задания({count_not_ready_urls})', callback_data='Ссылки в работе-0')])
        inline_keyboard.append([InlineKeyboardButton(text=f'✔Выполнено({count_ready_urls})', callback_data='Выполнено')])
    #собираем клавиатуру и отправляем одно сообщение
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    

#ВЫПОЛНЕНО
@client.callback_query(F.data.startswith("Выполнено"))
async def ready_urls(callback: CallbackQuery):
    #формируем стартовую клавиатуру, которую будем отправлять
    count_not_ready_urls = await get_count_not_ready_urls_for_user(callback.from_user.id)
    count_ready_urls = await get_count_ready_urls_for_user(callback.from_user.id)
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text=f'⚡Новые задания({count_not_ready_urls})', callback_data='Ссылки в работе-0')])
    inline_keyboard.append([InlineKeyboardButton(text=f'✔Выполнено({count_ready_urls})', callback_data='Выполнено')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    #обновляем данные пользователя
    await update_db(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
    #получаем выполненные ссылки
    list_ready_urls = await get_list_ready_urls_for_user(callback.from_user.id)  
    #глобальная переменная для индесирования ссылок
    global_index = 0
    #если ссылки есть
    #отправляем тесктовые сообщения со всеми ссылками
    if len(list_ready_urls) > 0:
        #удаляем старое сообщение
        try:
            await callback.message.delete()
        except:
            pass #старые сообщения(более двух дней) не удаляются
        #отправляем сообщение, что будут выведены выполненные ссылки
        await callback.message.answer("Обработанные ссылки")
        #пока прошли не по всем ссылка
        while global_index <= len(list_ready_urls) - 1: 
            #сообщение для отправки
            message_text = ""
            #формируем сообщение из 10 ссылок
            for _ in range(10):
                if global_index > len(list_ready_urls) - 1:
                    break
                #получаем url по urlname
                url = await get_url_by_urlname(list_ready_urls[global_index])
                message_text += f"#{global_index+1} | {url}\n"
                global_index += 1
            #отправляем сообщение
            await callback.message.answer(message_text, disable_web_page_preview=True)
        #отправляем последнее сообщение с клавиатурой
        await callback.message.answer("Добро пожаловать!", reply_markup=keyboard)
    #если нет ссылок
    #редактируем сообщение, что нет выполненных ссылок
    else:
         await callback.message.edit_text("❗️Нет выполненных ссылок", reply_markup=keyboard)
    

#Взяться в работу для блокировки ссылок
@client.callback_query(F.data.startswith("url"))
async def url_processing(callback: CallbackQuery):
    #обновляем данные пользователя
    await update_db(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
    #получаем имя ссылки из-под кнопки
    urlname = callback.data[4:]
    #получаем url по urlname
    url = await get_url_by_urlname(urlname)
    #формируем новое сообщение
    message_text = f"""Продолжаем🔥

❗️Блокируем страницу ЦИПСО распространяющую проукраинскую пропаганду, фейки, дискредитирование власти и МО РФ.

📌Инструкция:

1️⃣ Переходим по ссылке:
{url};

2️⃣ Нажимаем кнопку "Пожаловаться";

3️⃣Выбираем нужную графу;

4️⃣Комментарий в свободной форме; 

🚩Отправляем жалобу

Задание выполнено!

Нажатие на кнопку - ❗️❗️❗️отчитаться без ПОДТВЕРЖДЕНИЯ"""
    #кнопка для подтверждения выполенения задания
    keyboard = []
    keyboard.append([InlineKeyboardButton(text='Отчитаться о выполнении', callback_data=f'ready:{urlname}')])
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data='Ссылки в работе-0')])
    #собираем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(message_text, reply_markup=keyboard, disable_web_page_preview=True)
    

#отчитаться о блокировке ссылки
@client.callback_query(F.data.startswith("ready"))
async def ready_url(callback: CallbackQuery):
    #получаем имя url ссылки
    urlname = callback.data[6:]
    #обновляем бд - ссылка обработана
    await report_by_link(callback.from_user.id, urlname)
    #получаем сколько ссылок сделано и сколько не сделано конкретным пользователем
    count_not_ready_urls = await get_count_not_ready_urls_for_user(callback.from_user.id)
    count_ready_urls = await get_count_ready_urls_for_user(callback.from_user.id)
    #создаём кнопки для клавы
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton(text=f'⚡Новые задания({count_not_ready_urls})', callback_data='Ссылки в работе-0')])
    inline_keyboard.append([InlineKeyboardButton(text=f'✔Выполнено({count_ready_urls})', callback_data='Выполнено')])
    #собираем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await callback.message.edit_text("Добро пожаловать!", reply_markup=keyboard)
    await callback.answer("Успешно! Спасибо, что Вы с нами🥰", show_alert=True)
    
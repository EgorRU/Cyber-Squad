from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from config import bot


#проверка на админа
async def is_admin(id_user, username):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT user_id FROM data WHERE user_id=? and is_admin=?",(id_user, 1)).fetchone()
    if data != None:
        return True
    data = cur.execute(f"SELECT username FROM data WHERE username=? and is_admin=?",(username, 1)).fetchone()
    base.close()
    if data != None:
        return True
    return False
     

#обновление id или username пользователя
async def update_db(id_user, fullname, username):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT * FROM data WHERE user_id=? or username=?",(id_user, username)).fetchone()
    if data == None:
        cur.execute("INSERT INTO data values (?,?,?,?)", (id_user, 0, fullname, username))
    else:
        cur.execute("UPDATE data set fullname=?, username=?, user_id=? where user_id=? or username=?", (fullname, username, id_user, id_user, username))
    base.commit()
    base.close()


#получить всех пользователей не админов для рассылки
async def get_all_id_user():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT user_id FROM data WHERE is_admin=?",(0,)).fetchall()
    base.close()
    if data != None:
        return [value[0] for value in data]
    return []
        

async def add_admin(username):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    id_user_from_db = cur.execute(f"SELECT username FROM data WHERE username=?", (username,)).fetchone()
    if id_user_from_db != None:
        cur.execute("UPDATE data SET is_admin=? WHERE username=?",(1, username))
    else:
        cur.execute("INSERT INTO data(is_admin, fullname, username) values (?,?,?)", (1, "unknown", username))
    base.commit()
    base.close()
    return True


async def delete_admin(user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    if user.isdigit():
        id_user_from_db = cur.execute(f"SELECT user_id FROM data WHERE user_id=?", (int(user), )).fetchone()
        if id_user_from_db != None:
            cur.execute("UPDATE data SET is_admin=? WHERE user_id=?",(0, user))
    else:
        id_user_from_db = cur.execute(f"SELECT username FROM data WHERE username=?", (user[1:], )).fetchone()
        if id_user_from_db != None:
            cur.execute("UPDATE data SET is_admin=? WHERE username=?",(0, user[1:]))
    base.commit()
    base.close()
    if id_user_from_db != None:
        return True
    return False


#получить список всех админов
async def get_admin():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    all_id_admin = cur.execute(f"SELECT user_id, fullname, username FROM data WHERE is_admin=?", (1,)).fetchall()
    if len(all_id_admin) > 0:
        text_message = ""
        index = 1
        inner_keyboard = []
        inline_keyboard = []
        for admin in all_id_admin:
            id_user, fullname, username = admin
            username = f"@{username}" if username != None and username != "" else ""
            text_message += f"{index}) ✅{fullname}"
            if username == "":
                text_message += "\n"
            else:
                text_message += f" | {username}\n"
            if id_user == None:
                id_user = username
            inner_keyboard.append(InlineKeyboardButton(text=f'{index})Удалить {username if username!="" else fullname}', callback_data=f'deleteadmin{id_user}'))
            index += 1
            if len(inner_keyboard)>=2:
                inline_keyboard.append(inner_keyboard)
                inner_keyboard = []
        else:
            inline_keyboard.append(inner_keyboard)
        inline_keyboard.append([InlineKeyboardButton(text='❗Добавить администратора', callback_data='Добавить админа')])
        inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data='Назад')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return keyboard, text_message
    else:
        return None, "Нет администраторов"


async def set_new_url(new_url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    data = cur.execute(f"SELECT url FROM urls WHERE url=?",(new_url,)).fetchone()
    if data == None:
        cur.execute("INSERT INTO urls values (?,?)", (new_url, 0))
    base.commit()
    base.close()
    if data == None:
        return True
    return False
        

async def get_url():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    data = cur.execute(f"SELECT url, block FROM urls").fetchall()
    base.close()
    if data == None:
        return []
    return data


#изменить статус ссылки на заблокированный
async def update_url(url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    if len(url)<64:
        data = cur.execute(f"SELECT block FROM urls where url=?", (url,)).fetchone()
        if data != None:
            cur.execute(f"UPDATE urls set block=? where url=?",(1, url))
        base.commit()
        base.close()
        if data == None or data[0]==1:
            return False
        return True
    else:
        data = cur.execute(f"SELECT block FROM urls where url like '%{url}%'").fetchone()
        if data != None:
            cur.execute(f"UPDATE urls set block=? where url like '%{url}%'",(1,))
        base.commit()
        base.close()
        if data == None or data[0]==1:
            return False
        return True


async def delete_url(url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    data = cur.execute(f"SELECT * FROM urls where url=?", (url,)).fetchone()
    if data != None:
        cur.execute(f"DELETE from urls where url=?",(url,))
    base.commit()
    base.close()
    if data == None or data[0]==1:
        return False
    return True


async def edit_url(old_url, new_url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    data = cur.execute(f"SELECT * FROM urls where url=?", (new_url,)).fetchone()
    if data == None:
        cur.execute(f"UPDATE urls set url=? where url=?", (new_url, old_url))
    base.commit()
    base.close()
    return True


async def swap_status_url(url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS urls(url PRIMARY KEY, block integer)")
    base.commit()
    data = cur.execute(f"SELECT block FROM urls where url=?", (url,)).fetchone()
    if data != None:
        if data[0] == 1:
            cur.execute(f"UPDATE urls set block=? where url=?",(0, url))
        else:
            cur.execute(f"UPDATE urls set block=? where url=?",(1, url))
    base.commit()
    base.close()


#получить клавиатуру и текст сообщения для отправки
#message - для callback, чтобы понимать, для чего вызвана клава - для просмотра, удаления, редактирования, длинна message 4 символа
async def get_keyboard_and_message_text(message):
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
            inner_keyboard.append(InlineKeyboardButton(text=f'{index}{string}', callback_data=f'{message}{link if len(link)<60 else link[-60:]}'))
            index += 1
            if len(inner_keyboard)>4:
                inline_keyboard.append(inner_keyboard)
                inner_keyboard = []
        else:
            inline_keyboard.append(inner_keyboard)
        if message != 'show':
            inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data='Редактирование таблицы')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return keyboard, text_message
    else:
        return None, "Нет необработанных ссылок"
    

#рассылка
async def mailing():
    all_id_user = await get_all_id_user()
    keyboard, text_message = await get_keyboard_and_message_text("show")
    for id_user in all_id_user:
        try:
            await bot.send_message(id_user, f"Появились новые ссылки:\n{text_message}", reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass

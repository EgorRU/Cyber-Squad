import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def is_admin(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT user_id FROM data WHERE user_id=? and is_admin=?",(id_user, 1)).fetchone()
    base.close()
    if data != None:
        return True
    return False
     

async def update_db(id_user, fullname, username):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT user_id FROM data WHERE user_id=?",(id_user,)).fetchone()
    if data == None:
        cur.execute("INSERT INTO data values (?,?,?,?)", (id_user, 0, fullname, username))
    else:
        cur.execute("UPDATE data set fullname=?, username=? where user_id=?", (fullname, username, id_user))
    base.commit()
    base.close()
    if data == None:
        return True
    return False


async def get_all_id_user():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    data = cur.execute(f"SELECT user_id FROM data WHERE is_admin=?",(0,)).fetchall()
    base.close()
    if data != None:
        return [value[0] for value in data]
    return []
        

async def add_admin(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    id_user_from_db = cur.execute(f"SELECT user_id FROM data WHERE user_id=?", (id_user,)).fetchone()
    if id_user_from_db != None:
        cur.execute("UPDATE data SET is_admin=? WHERE user_id=?",(1, id_user))
    else:
        cur.execute("INSERT INTO data values (?,?,?,?)", (id_user, 1, "unknown", "unknown"))
    base.commit()
    base.close()
    return True


async def delete_admin(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
    base.commit()
    id_user_from_db = cur.execute(f"SELECT user_id FROM data WHERE user_id=?", (id_user, )).fetchone()
    if id_user_from_db != None:
        cur.execute("UPDATE data SET is_admin=? WHERE user_id=?",(0, id_user))
    base.commit()
    base.close()
    if id_user_from_db != None:
        return True
    return False


async def get_admin():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    base.execute("CREATE TABLE IF NOT EXISTS data(user_id integer PRIMARY KEY, is_admin integer, fullname TEXT, username TEXT)")
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
            text_message += f"{index}) ✅{fullname} | {username}\n"
            inner_keyboard.append(InlineKeyboardButton(text=f'Удалить {fullname}', callback_data=f'admin{id_user}'))
            index += 1
            if len(inner_keyboard)>=2:
                inline_keyboard.append(inner_keyboard)
                inner_keyboard = []
        else:
            inline_keyboard.append(inner_keyboard)
        inline_keyboard.append([InlineKeyboardButton(text='❗Добавить админа', callback_data='Добавить админа')])
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

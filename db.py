import sqlite3
from config import bot


#получение списка всех пользователей
async def get_list_users(Full_users=True):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    #получаем список всех пользователей
    if Full_users:
        data = cur.execute("SELECT id_user FROM users").fetchall()
    #получаем список только рядовых сотрудников
    else:
        data = cur.execute("SELECT id_user FROM users where is_admin=?", (0,)).fetchall()
    base.close()
    #если пользователей нет, то возвращаем пустой список
    if data == None:
        return []
    #иначе возвращаем список из id_user
    else:
        return [user[0] for user in data] #из бд возвращается список из кортежей


#получение списка всех ссылок
async def get_list_urls():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT urlname FROM urls").fetchall()
    base.close()
    #если ссылок нет, то возвращаем пустой список
    if data == None:
        return []
    #иначе возвращаем список urlname
    else:
        return [urlname[0] for urlname in data] #из бд возвращается список из кортежей


#обновление всей бд
async def update_db(id_user, fullname, username):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT * FROM users WHERE id_user=?",(id_user,)).fetchone()
    #если пользователя нет, то добавляем его и показываем ему все ссылки
    if data == None:
        #добавление пользователя в бд
        cur.execute("INSERT INTO users values (?,?,?,?,?)", (id_user, fullname, username, 0, 0))
        base.commit()
        #получаем список всех url
        list_urlname = await get_list_urls()
        #каждый url добавляем каждому пользователю
        for urlname in list_urlname:
            cur.execute("INSERT INTO users_urls values (?,?,?)", (id_user, urlname, 0))
            base.commit()
    #если пользователь есть, то обновляем его имя
    else:
        cur.execute("UPDATE users set fullname=?, username=? where id_user=?", (fullname, username, id_user))
        base.commit()
    base.close()
    

#проверка на админа
async def is_admin(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT id_user FROM users WHERE id_user=? and is_admin=?",(id_user, 1)).fetchone()
    base.close()
    #если нашли запись в бд => админ
    if data != None:
        return True
    return False
     

#количество необработанных ссылок для конкретного пользователя
async def get_count_not_ready_urls_for_user(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT count(*) FROM users_urls where id_user=? and is_ready=?", (id_user, 0)).fetchone()
    base.close()
    return data[0]


#количество обработанных ссылок для конкретного пользователя
async def get_count_ready_urls_for_user(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT count(*) FROM users_urls where id_user=? and is_ready=?", (id_user, 1)).fetchone()
    base.close()
    return data[0]


#рассылка всем рядовым пользователям
async def mailing():
    list_users = await get_list_users(False) #False = не делаем рассылку администраторам
    for user in list_users:
        try:
            await bot.send_message(user, "Появились новые ссылки\n\n/start - узнать новые задачи")
        except:
            pass #пользователь добавил бота в чс


#добавление новой ссылки в базу данных
async def set_new_url(new_url):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute(f"SELECT url FROM urls WHERE url=?",(new_url,)).fetchone()
    #если ссылка новая, то добавляем её
    if data == None:
        count_url = cur.execute("SELECT count(*) FROM urls").fetchone()
        #номер следующей ссылки
        next_number_for_url = int(count_url[0]) + 1 #из бд возвращается кортеж
        cur.execute("INSERT INTO urls values (?,?,?)", (f"Ссылка №{next_number_for_url}", new_url, 0))
        #получаем список всех пользователей
        list_users = await get_list_users()
        #всем пользователям добавляем её как невыполненную
        for user in list_users:
            cur.execute("INSERT INTO users_urls values (?,?,?)", (user, f"Ссылка №{next_number_for_url}", 0))
            base.commit()
    base.close()
    #если ссылка новая
    if data == None:
        return True
    return False
        

#получения списка необработанных ссылок для конкретного пользователя
async def get_list_urls_in_work_for_user(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT urlname FROM users_urls where id_user=? and is_ready=?", (id_user, 0)).fetchall()
    base.close()
    #если ссылок нет, то возвращаем пустой список
    if data == None:
        return []
    #иначе возвращаем список urlname
    else:
        return [urlname[0] for urlname in data] #из бд возвращается список из кортежей
    

#получения списка обработанных ссылок для конкретного пользователя
async def get_list_ready_urls_for_user(id_user):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT urlname FROM users_urls where id_user=? and is_ready=?", (id_user, 1)).fetchall()
    base.close()
    #если ссылок нет, то возвращаем пустой список
    if data == None:
        return []
    #иначе возвращаем список urlname
    else:
        return [urlname[0] for urlname in data] #из бд возвращается список из кортежей
    

#получение ссылки по её имени
async def get_url_by_urlname(urlname):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT url FROM urls where urlname=?", (urlname, )).fetchone()
    base.close()
    #если ссылки нет - возвращаем None
    if data == None:
        return None
    #иначе url
    else:
        return data[0] #из бд возвращается список из кортежей
    

#изменение бд - ссылка обработана конкретным пользователем
async def report_by_link(id_user, urlname):
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    cur.execute("UPDATE urls set count_ready=count_ready+1 where urlname=?", (urlname,))
    base.commit()
    cur.execute("UPDATE users set count_ready_url=count_ready_url+1 where id_user=?", (id_user,))
    base.commit()
    cur.execute("UPDATE users_urls set is_ready=? where id_user=? and urlname=?", (1, id_user, urlname))
    base.commit()
    base.close()
    

#получение всех данных из таблицы urls
async def get_full_urls():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    data = cur.execute("SELECT * FROM urls").fetchall()
    base.close()
    return data
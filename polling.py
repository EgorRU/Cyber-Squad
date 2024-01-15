import gspread
import asyncio
from db import get_full_urls


gc = gspread.service_account(filename='token.json')
sh = gc.open_by_key('16a_HMnxGVVHJHqWWQ1ZrzX-9AeqR3hTIyniRxnLGFqk')
worksheet = sh.worksheet("Ссылки")


async def main():
    while True:
        try:
            #получение всех ссылок
            full_urls = await get_full_urls()
            #начинаем со 2 строки(1 строка - названия столбиков)
            index_in_google_table = 2
            #заполнение таблицы
            for _ in range(len(full_urls)):
                urlname, url, count_ready = full_urls[index_in_google_table-2]
                worksheet.update_cell(index_in_google_table, 1, urlname)
                worksheet.update_cell(index_in_google_table, 2, url)
                worksheet.update_cell(index_in_google_table, 3, count_ready)
                await asyncio.sleep(3.1)
                index_in_google_table += 1
            #если остались ячейки снизу, заполненный чем-то, то удаляем их
            val = worksheet.cell(index_in_google_table, 1).value
            #пока не пусто
            while val != None:
                worksheet.update_cell(index_in_google_table, 1, "")
                worksheet.update_cell(index_in_google_table, 2, "")
                worksheet.update_cell(index_in_google_table, 3, "")
                index_in_google_table += 1
                val = worksheet.cell(index_in_google_table, 1).value
            #уходим в сон, гугл апи много запросов не терпит
            await asyncio.sleep(30)
        #если превысили лимит в минуту
        except:
            await asyncio.sleep(60)
        

if __name__ == '__main__':
    asyncio.run(main())

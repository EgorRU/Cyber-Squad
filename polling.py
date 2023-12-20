import gspread
import asyncio
from db import get_url


gc = gspread.service_account(filename='token.json')
sh = gc.open_by_key('16a_HMnxGVVHJHqWWQ1ZrzX-9AeqR3hTIyniRxnLGFqk')
worksheet = sh.worksheet("Ссылки")


async def main():
    while True:
        try:
            #получение всех ссылок
            url_tuples = await get_url()
            index = 1
            #заполнение таблицы
            for url_tuple in url_tuples:
                url = url_tuple[0]
                is_block = "yes" if url_tuple[1]==1 else "no"
                worksheet.update_cell(index, 1, url)
                worksheet.update_cell(index, 2, is_block)
                if is_block=="yes":
                    worksheet.format(f"A{index}:B{index}", {
                    "backgroundColor": {
                        "red": 0.0,
                        "green": 10.0,
                        "blue": 0.0
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "fontSize": 11,
                    }
                    })
                else:
                    worksheet.format(f"A{index}:B{index}", {
                    "backgroundColor": {
                        "red": 10.0,
                        "green": 0.0,
                        "blue": 0.0
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "fontSize": 11,
                    }
                    })
                await asyncio.sleep(2.5)
                index += 1
            #если остались ячейки снизу, заполненный чем-то, то удаляем их
            val = worksheet.cell(index, 1).value
            while val != None:
                worksheet.update_cell(index, 1, "")
                worksheet.update_cell(index, 2, "")
                worksheet.format(f"A{index}:B{index}", {
                    "backgroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 1
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "fontSize": 10,
                    }
                    })
                index += 1
                val = worksheet.cell(index, 1).value
            await asyncio.sleep(30)
        except:
            await asyncio.sleep(60)
        

if __name__ == '__main__':
    asyncio.run(main())

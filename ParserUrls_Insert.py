import parsing
from threading import *
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import datetime
URLS =['https://europharma.kz/catalog/lekarstvennye-sredstva?segment=available',
       'https://europharma.kz/catalog/vitaminy-i-bady?segment=available',
       'https://europharma.kz/catalog/izdelia-med-naznacenia?segment=available',
       'https://europharma.kz/catalog/mat-i-ditya?segment=available',
       'https://europharma.kz/catalog/krasota-i-gigiena?segment=available']

"""parsing url"""
# for index in range(0, len(URLS)):
#     filename =f"urls_sub_cat_{index}.txt"
#     print(index)
#     parsing.get_list_of_urls(filename)



conn = parsing.connection
cur = conn.cursor()
cur2 =conn.cursor()

# file = open("city.txt", encoding='utf-8', mode='r')
# for line in file:
#     x = line.split(",")
#     print(x[0])
#     query=f"INSERT INTO CITY(city, url) VALUES ('{x[0]}', '{x[1]}')"
#     cur.execute(query)
#     conn.commit()


"""parsing content"""
# # cur.execute("select url from urls")
# col = cur.fetchall()
# print(len(col))
# count=0
#
# for c in col:
#             html=parsing.get_html(c[0])
#             x = c[0].split(".kz/")
#             parsing.get_content_of_items(html, x[1])
#             count +=1
#             print(count)

query = f"SELECT city, url FROM CITY where id>4"


cur.execute(query)
city_row = cur.fetchall()
q2 = f"SELECT id, url from product"
cur.execute(q2)
product_row = cur.fetchall()


def write_item_url_to_txt(city, filename):
    file = open(filename, encoding='utf-8', mode ='a')
    for product in product_row:
        u = city[1].replace("\n", "")
        url = u + product[1]
        text = f"{city[0]},{url},{product[0]}\n"
        file.write(text)


def inserting(line):
            r = line.split(",")
            url =r[1]
            html = parsing.get_html(url)
            if html:
                list = parsing.get_price(html)
                try:
                    q3 = f"INSERT INTO price (city, product_id, price, availability, url, date ) VALUES ('{r[0]}', {r[2]},'{list[0]}','{list[1]}', '{url}', '{datetime.date.today()}')"
                    cur.execute(q3)
                    conn.commit()
                    print('Inserted')
                except Exception as ex:
                    print(ex)


with open("url_items.txt", encoding="utf-8", mode='r') as file:
    # for line in file:
    #     inserting(line)
    with ThreadPoolExecutor(max_workers=100) as executor:
        t1 = [executor.submit(inserting, line) for line in file]

# filename = "url_items.txt"
#
# for r in city_row:
#     write_item_url_to_txt(r, filename)




# with ThreadPoolExecutor(max_workers=4) as executor:
#     t1 = executor.submit(execute_query_1, query1)
    # t2 = executor.submit(execute_query_2, query2)


# #
# t1.start()
# t2.start()
# t3.start()
# t4.start()

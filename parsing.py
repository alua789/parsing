import requests
from bs4 import BeautifulSoup
import psycopg2

connection = psycopg2.connect(
    host = '127.0.0.1',
    database='Europharma',
    user = 'postgres',
    password = 'admin123',
    port= '5432',

)
cursor = connection.cursor()


URL='https://europharma.kz/catalog/analgetiki?segment=available'
HEADERS={'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
         'accept':'*/*'}
HOST='https://europharma.kz'
URLS = [
    'https://europharma.kz/catalog/analgetiki?page=3',
    'https://europharma.kz/catalog/antibiotiki',
]



def get_html(url, params=None):
    r=requests.get(url, headers=HEADERS, params=params)
    return r


def get_url_sub_categories(html, filename):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('li', class_='subcategories__item')
    file = open(filename, "w")
    count = 0
    for item in items:
        count += 1
        file.write(HOST + item.find('a', class_='subcategories__link').get('href')+'\r')


def get_url_catalog(html, filename):
    file = open(filename, 'a')
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('li', class_="menu__item")
    for item in items:
        text = item.find('a', class_='menu__link').get('href')+'\n'
        file.write(text)


def get_list_of_urls(filename):
    file = open(filename)
    for url in file:
        html1 = get_html(url)
        if html1.status_code == 200:
            pages_count = page_count(html1)
            for page in range(1, (pages_count + 1)):
                html2 = get_html(url, params={'page': page})
                print(f"parsinf page of {page}  of the file {filename}")
                if html2.status_code == 200:
                    Url_items = get_url_item(html2)
                    print(Url_items)
                    insert_urls(Url_items)


def insert_urls(listUrl):
    for url in listUrl:
        """ query code """
        query = f"insert into  public.urls (url, news) values ('{url}', 1)"
        cursor.execute(query)
        connection.commit()


def get_url_item(html):
     if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='catalog-list__item')
        urls_sub_categories_sub = []
        for item in items:
            url_text = HOST + item.find('a').get('href')
            urls_sub_categories_sub.append(url_text)
        return urls_sub_categories_sub
     else:
         print("ERROR")


def get_content_of_items(html, url):
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='product-detail')
        cat = soup.find_all('li', class_='breadcrumb__item')
        catalog = f"{cat[2].find('span').get_text()}"
        category = cat[3].find('span').get_text()

        count = 0
        for item in items:
            count += 1

            key = item.find_all('dt', class_='characteristic__item')
            value = item.find_all('dd', class_='characteristic__value')
            title=f"{item.find('h1', class_='product__title').get_text()}"

            if title.find("'"):
                title = title.replace("'", "''")
            if len(key) == 4:
                manufacturer = value[3].get_text()
                if manufacturer.find("'"):
                    manufacturer = manufacturer.replace("'", "''")

                query= f'INSERT INTO public.product( title, category, sub_category, availability, model, country, manufacturer, url)VALUES (' \
                       f"'{title}', '{catalog}','{category}', '{value[0].get_text()}', '{value[1].get_text()}', '{value[2].get_text()}', '{manufacturer}', '{url}')"
                cursor.execute(query)
                connection.commit()
            elif len(key) == 3:
                query = f'INSERT INTO public.product( title, category, sub_category, availability, model, country, url)VALUES ('  \
                        f"'{title}', '{catalog}', " \
                        f"'{category}', '{value[0].get_text()}', '{value[1].get_text()}', '{value[2].get_text()}','{url}')"
                cursor.execute(query)
                connection.commit()
            elif len(key) == 2:
                query = f'INSERT INTO public.product( title, category, sub_category, availability, model, url)VALUES (' \
                        f"'{title}', '{catalog}', " \
                        f"'{category}', '{value[0].get_text()}', '{value[1].get_text()}', '{url}')"
                cursor.execute(query)
                connection.commit()


def get_price(html):
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='product__price')
        value = soup.find_all('dd', class_='characteristic__value')
        text = " "
        array =[]
        for item in items:
            pr = item.find('span', class_='product__price-value').get_text()
            pc = item.find('span', class_='product__currency').get_text()
            text = f"{pr} {pc}"
        array.append(text)
        array.append(value[0].get_text())
        return array
    else:
        return "null"




def page_count( html):
        soup = BeautifulSoup(html.text, 'html.parser')
        page = soup.find_all('li', class_='pagination__item')
        if page:
            return int(page[-2].get_text())
        else:
            return 1





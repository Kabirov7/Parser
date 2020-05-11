import mysql.connector
import requests
from bs4 import BeautifulSoup


URL = 'http://timemovie.ru/top-100-serialy'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}

#FINAL STEP. Saving file in .csv
# def save_file(items, path):
#     with open(path, 'w', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(['Название', 'Ccылка', ])
#         for item in items:
#             writer.writerow([item['title'], item['link'],])
def save_sql(items):
    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='films')
    mycursor = db.cursor()
    mycursor.execute('DROP TABLE serial')
    mycursor.execute('CREATE TABLE serial(ID int PRIMARY KEY AUTO_INCREMENT, title VARCHAR(70), link VARCHAR(100))')

    for i in items:
        sqlFormula = 'INSERT INTO serial(title, link) VALUES (%s,%s)'
        films = ([i['title'], i['link']])
        mycursor.execute(sqlFormula,films)
    db.commit()

#firt step. get html
def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params=params)
    return r


#third step. init func which parsing content
def get_content(html):

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='serial_x')

    serial = []
    for i in items:
        serial.append({
            'title': i.find('a').get_text(),
            'link': i.find('a').get('href')
        })
    return serial

#secon step. inint main func parse() where will order all functions
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        serial = []
        html = get_html(URL, params=None)
        serial.extend(get_content(html.text))
        #transmit data(first param) and path(second param) where we will save file
        save_sql(serial)
        print(f'RECIVED: {len(serial)} SERIALS')
    else:
        print('ERROR')

parse()
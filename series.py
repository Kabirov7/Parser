import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://timemovie.ru/top-100-serialy'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}
FILE = 'serial.csv'

#FINAL STEP. Saving file in .csv
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ccылка', ])
        for item in items:
            writer.writerow([item['title'], item['link'],])

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
        save_file(serial, FILE)
        print(f'RECIVED: {len(serial)} SERIALS')
    else:
        print('ERROR')

parse()
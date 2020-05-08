import requests
from bs4 import BeautifulSoup
import csv
import time

URL = 'http://timemovie.ru/top-100-serialy'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}

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
    print(serial)
    print(len(serial))


#secon step. inint main func parse() where will order all functions
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('ERROR')

parse()
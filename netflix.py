import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://zetflix.cc/serials'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://zetflix.cc'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='swchItem')[-2].find_next('span').get_text()
    if pagination:
        return int(pagination)
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')

    serial = []
    for i in items:
        serial.append({
            'title': i.find('div', class_='vid-t').get_text(),
            'desc': i.find('div', class_='vid-mes').get_text(),
            'link': HOST + i.find_previous('a').get('href'),
        })
    return serial



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        serial=[]
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Parsing {page}/{pages_count}')
            html = get_html(URL, params={'page': page})
            serial.extend(get_content(html.text))
        print(serial)

parse()

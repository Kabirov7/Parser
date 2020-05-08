import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.kinoafisha.info/rating/movies/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://www.kinoafisha.info'
FILE = 'FILMS.csv'

def save_file(items, path):
    with open(path, 'w', newline='') as  file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Описание', 'Рэйтинг по <<KinoAfisha>>', 'Год и страна', 'Жанр', 'Продюсер',])
        for item in items:
            writer.writerow([item['title'], item['link'], item['rating'], item['year_country'], item['genre'], item['producer'], ])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pager_item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='films_right')

    films = []
    for item in items:
        films.append({
            'title': item.find('a', class_='films_name').get_text(),
            'link': HOST + item.find('a', class_='films_name').get('href'),
            'rating': item.find('span', class_='rating_num').get_text(),
            'year_country': item.find('span', class_='films_info').get_text(),
            'genre': item.find_all('span', class_='films_info')[1].get_text(),
            'producer': item.find_all('span', class_='films_info')[-1].get_text().lstrip('\n').replace(' ', '')

        })

    return films

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        films = []
        pages_count = get_pages_count(html.text)
        for page in range(pages_count):
            print(f'Cтраницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            films.extend(get_content(html.text))
            # films = get_content(html.text)
        save_file(films, FILE)
        print(f'Получено {len(films)} фильмов')
    else:
        print('error')


parse()
import csv
import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet

HOST = 'https://www.mashina.kg/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}



def get_html(url: str, category: str, headers: dict='', params: str=''):
    """ Функция для получения html кода """
    html = requests.get(
        url + category + '/all',
        headers=headers,
        params=params,
        verify=False
    )
    return html.text



def get_card_from_html(html: str) -> ResultSet:
    """ Функция для получения карточек из html-кода """
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('div', class_='list-item list-label')
    return cards



def parse_data_from_cards(cards: ResultSet) -> list:
    """ Фильтрация данных из карточек """
    result = []
    for card in cards:
        try:
            image_link = list(card.find('a').find('div', class_='thumb-item-carousel').find_all('img', class_='lazy-image'))[0].get('data-src')
            # image_link = image.get('data-src')
        except AttributeError:
            image_link = 'Нет картинки'

        # единственное проблемное авто - <img class="lazy-image visible" alt="Фото авто Volkswagen Vento" title="" src="https://im.mashina.kg/tachka/images//1/7/f/17f704208220317ddebfce5e1691429c_240x180.jpg" style="display: block;">
        except IndexError:
            image_link = "https://im.mashina.kg/tachka/images//1/7/f/17f704208220317ddebfce5e1691429c_240x180.jpg"
        try:
            title = card.find('a').find('div', class_='block title').find('h2').text.strip()
        except AttributeError:
            title = ''

        try:
            price = card.find('a').find('div', class_='block price').find('p').text.split('\n')[1]
        except AttributeError:
            price = ''
        
        try:
            description1 = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p',class_='year-miles').text.strip() + ', '
        except AttributeError:
            description1 = ''

        try:
            description2 = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p',class_='body-type').text.strip() + ', '
        except AttributeError:
            description2 = ''

        try:
            description3 = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='volume').text.strip()
        except AttributeError:
            description3 = ''

        description = description1 + description2 + description3

        obj = {
            'title': title, 
            'price': price,
            'description': description,
            'image_link': image_link,
        }

        result.append(obj)
    return result



def write_to_csv(data: list):
    """ Запись данных в csv файл """
    fieldnames = ['title', 'price', 'description', 'image_link']
    with open('cars_small.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
        


def get_last_page(category):
    """ Получение количества страниц """
    html = get_html(HOST, category)
    soup = BeautifulSoup(html, 'lxml')
    total_pages = soup.find('div', class_='search-results-table').find('nav').find('ul', class_='pagination').find_all('li', class_='page-item')[-1]
    last_page = total_pages.find('a').get('data-page')
    return int(last_page)



def main(category):
    result = []
    # for page in range(1, get_last_page(category)+1):
    for page in range(1, get_last_page(category)-880):
        html = get_html(HOST, category, params=f'page={page}', headers=HEADERS)
        cards = get_card_from_html(html)
        list_of_cards = parse_data_from_cards(cards)
        result.extend(list_of_cards)
    write_to_csv(result)



if __name__ == '__main__':
    main('search')
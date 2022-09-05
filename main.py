"""
1. Получить html-код страницы
2. Получить карточки из html-кода
3. Распарсить данные с карточек
4. Полученные данные записать в csv
"""




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
    # print(cards)
    return cards



def parse_data_from_cards(cards: ResultSet) -> list:
    """ Фильтрация данных из карточек """
    result = []
    for card in cards:
        try:
            image_link = card.find('a').find('div', class_='thumb-item-carousel brazzers-daddy').find('div', class_='image-wrap').find('img', class_='lazy-image visible').get('src')
        except AttributeError:
            image_link = 'Нет картинки'
    
        try:
            title = card.find('a').find('div', class_='block title').find('h2').text.strip()
        except AttributeError:
            title = ''

        try:
            price = card.find('a').find('div', class_='block price').find('p').text.split('\n')[1]
        except AttributeError:
            price = ''
        
        try:
            description1 = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p',class_='year-miles').text.strip()
        except AttributeError:
            description1 = ''

        try:
            description2 = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p',class_='body-type').text.strip()
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
    with open('cars.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
        


def get_last_page(category):
    html = get_html(HOST, category)
    soup = BeautifulSoup(html, 'lxml')
    total_pages = soup.find('div', class_='search-results-table').find('nav').find('ul', class_='pagination').find_all('li', class_='page-item')[-1]
    last_page = total_pages.find('a').get('data-page')
    print(int(last_page))
    return int(last_page)



def main(category):
    result = []
    for page in range(1, get_last_page(category)+1):
        html = get_html(HOST, category, params=f'page={page}', headers=HEADERS)
        cards = get_card_from_html(html)
        list_of_cards = parse_data_from_cards(cards)
        result.extend(list_of_cards)
    write_to_csv(result)



if __name__ == '__main__':
    main('search')



'''
# Версия с урока


def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    html = requests.get(url, headers=headers, verify=False)
    # print(response.status_code)
    return html.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    print(soup.prettify())
    pages = soup.find('div', class_='search-results-table').find('nav').find('ul', class_='pagination')
    # print(pages)
    total_pages = str(pages.find_all('li', class_='page-item'))[-1]
    print(total_pages)
    # last_page = total_pages.find('a', class_='page-link').get('href')
    # last_page = total_pages.split('=')[-1]
    # print(last_page)
    # return int(last_page)

def write_to_csv(data):
    with open('mashina.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow((data['title'],
                         data['price'],
                         data['description'],
                         data['image']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='table-view-list image-view clr label-view')#.find('', class_='')
    products = product_list.find_all('div', class_='list-item list-label').find('a')
    # products1 = product_list.find_all('div', class_='list-item list-label ')
    # products2 = product_list.find_all('div', class_='list-item list-label new-line')

    for product in products:
        try:
            image = product.find('div', class_='image-wrap').find('img').get('src')
        except:
            image = ''

        try:
            title = product.find('div', class_='block title').find('h2').text.strip()
        except:
            title = ''

        try:
            price = product.find('div', class_='block price').find('p').find('br').text
        except:
            price = ''
        
        try:
            description = product.find('div', class_='block info-wrapper item-info-wrapper').find_all('p').text
        except:
            description = ''

        data = {'title': title, 'price': price, 'description': description, 'photo': image}
        write_to_csv(data)


def main(category):
    auto_url = 'https://www.mashina.kg/'
    auto1_url = 'https://www.mashina.kg/'

    pages = '?page='
   

    # last_page = get_total_pages(get_html(auto_url))

    # for page in range(1, last_page+1):
    #     url_with_page = auto_url + category + '/all/' + pages + str(page)
    #     html = get_html(url_with_page)
    #     get_page_data(html)
        

# main('search')
# main('commercialsearch')

auto_url = 'https://www.mashina.kg/search/all/'
last_page = get_total_pages(get_html(auto_url))
for page in range(1, 2):#last_page+1):  
    get_total_pages(get_html(auto_url + str(page)))
'''
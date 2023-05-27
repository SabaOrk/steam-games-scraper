import requests
from bs4 import BeautifulSoup
import csv
import time

session = requests.Session()
session.get('https://store.steampowered.com/')
session_id = session.cookies.get_dict()["sessionid"]

head = {'cookie': f'sessionid={session_id}'}


data = []
for i in range(1, 10):

    link = 'https://store.steampowered.com/search/results'
    param = {
        'term': 'game',
        'page': i
    }

    req = requests.get(link, params=param, headers=head)
    soup = BeautifulSoup(req.text, 'html.parser')

    content = soup.find('div', {'id': 'search_resultsRows'}).find_all('a')
    for i in content:
        url = i['href']
        title = i.find('div', 'col search_name ellipsis').text.strip().replace('\n', ' ')

        try:
            price = i.find('div', 'col search_price responsive_secondrow').text.strip()
        except Exception:
            price = 'discount from ' + i.find('span', {'style': 'color: #888888;'}).text.replace(' ', '.') + ' to ' + i.find('div', 'col search_price discounted responsive_secondrow').find('br').next_sibling.strip() + f" ({i.find('div', 'col search_discount responsive_secondrow').text.replace('-', '').strip()})"
        if price == '':
            price = 'none'

        release = i.find('div', 'col search_released responsive_secondrow').text
        if release == '':
            release = 'none'

        item = {
            'title': title,
            'price': price,
            'release': release,
            'link': url
        }
        data.append(item)
        time.sleep(5)

with open('steam_games.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)

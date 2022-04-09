# -*- coding: utf-8 -*-
import random

import requests
from bs4 import BeautifulSoup as Soup

from apis.main.answer_util import answer
from log import log

DOMAIN_URL = 'http://www.supertosty.ru'
WISHES_URL = 'http://www.supertosty.ru/pozhelaniya'


def get_wish():
    log('getting wish category...')
    response = requests.get(WISHES_URL)
    soup = Soup(response.text, 'html.parser')
    categories = soup.find('ul', {'class': 'side_menu_link'}).find_all('li')
    category = random.choice(categories).find('a')['href']
    link = DOMAIN_URL + category
    log('got wish category...')
    log('getting wish...')
    response = requests.get(link)
    soup = Soup(response.text, 'html.parser')
    wishes = soup.find('div', {'class': 'main_middle'}).find_all('div', {'class': 'tost_item'})
    wish = random.choice(wishes).find('div').text
    log('got wish...')
    wish = wish.encode('latin1').decode('cp1251').encode('utf8').replace('©', '')
    return '\n' + wish


def process_wish_answer(peer_id, chat):
    message = get_wish()
    answer(message, peer_id, chat)
import requests
from bs4 import BeautifulSoup as Soup

from apis.main.answer_util import quiet_answer
from log import log


def generate_excuse_text():
    log('getting excuse link...')
    domain = 'http://copout.me'
    response = requests.get(domain)
    soup = Soup(response.text, 'html.parser')
    path = soup.find('a',  {'class': 'btn-generation btn-open-excuse'})['data-href']
    link = domain + path
    log('got excuse link...')
    log('getting excuse text...')
    response = requests.get(link)
    soup = Soup(response.text, 'html.parser')
    text = soup.find('blockquote').text
    log('got excuse text...')
    return text


def process_excuse_answer(peer_id, chat):
    message = generate_excuse_text()
    quiet_answer(message, peer_id, chat)

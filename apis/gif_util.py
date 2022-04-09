import requests
import json

from apis.main.answer_util import gif_answer
from log import log

GIPHY_KEY = ''


def get_random_gif_url():
    log('getting gif..')
    url = 'http://api.giphy.com/v1/gifs/random?api_key=' + GIPHY_KEY
    response = requests.get(url)
    data = json.loads(response.text)['data']
    if not data or 'url' not in data:
        raise Exception('exception: no picture')
    log('got gif..')
    return data['fixed_height_small_url']
    # return data['image_url']


def process_gif_answer(peer_id, chat):
    gif_url = get_random_gif_url()
    gif_answer('', gif_url, peer_id, chat)

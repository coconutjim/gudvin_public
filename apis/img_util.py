import json
import random

import requests

from apis.main.answer_util import answer, img_answer
from log import log
from resources import images_ended

GCS_KEY = ''
GCS_ID = ''
NUM_IMAGES = '10'  # max 10


def get_img_url(query):
    log('getting pictures..')
    url = 'https://www.googleapis.com/customsearch/v1?key=' + GCS_KEY + '&cx=' + GCS_ID + '&q=' + query + \
          '&searchType=image&num=' + NUM_IMAGES
    response = requests.get(url)
    log('got pictures..')
    result = json.loads(response.text)
    if 'error' in result:
        return None
    items = result['items']
    res = list()
    for item in items:
        res.append(item['link'])

    return res[random.randint(0, len(res) - 1)]


def process_img_answer(query, peer_id, chat):
    img_url = get_img_url(query)
    if img_url is None:
        answer(images_ended, peer_id, chat)
        return
    img_answer('', img_url, peer_id, chat)

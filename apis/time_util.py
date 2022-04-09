# -*- coding: utf-8 -*-
import json

import requests

from apis.main.answer_util import answer
from log import log

TIMEZONEDB_API_KEY = ''
ZONE = 'Europe/Moscow'


def get_time():
    log('getting time...')
    method_url = 'http://api.timezonedb.com/v2/get-time-zone'
    params = dict(key=TIMEZONEDB_API_KEY, by='zone', zone=ZONE, format='json')
    response = requests.get(method_url, params=params)
    time = json.loads(response.text)['formatted']
    log('got time...')
    return time


def process_time_answer(peer_id, chat):
    time = get_time()
    answer(time, peer_id, chat)
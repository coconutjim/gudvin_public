# -*- coding: utf-8 -*-
import json
import random

import requests

import apis.main.twitter_api as api
from apis.main.answer_util import answer
from log import log

OLDEST_ADONEZH_ID = 286851644564594688
NEWEST_ADONEZH_ID = 0


def update_newest_id():
    log('updating adonezh id...')
    method_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    data = dict(screen_name='radioadonezh', count=1, trim_user='true', include_rts='false')
    response = requests.get(method_url, params=data, auth=api.TWITTER_OAUTH)
    result = json.loads(response.text)
    global NEWEST_ADONEZH_ID
    NEWEST_ADONEZH_ID = result[0]['id']
    log('updated adonezh id...')


def get_news():
    log('getting news...')
    method_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    tweet_id = random.randint(OLDEST_ADONEZH_ID, NEWEST_ADONEZH_ID)
    data = dict(screen_name='radioadonezh', count=1, max_id=tweet_id, trim_user='true', include_rts='false')
    response = requests.get(method_url, params=data, auth=api.TWITTER_OAUTH)
    result = json.loads(response.text)
    news = result[0]['text']
    log('got news...')
    return news


def process_news_adonezh_answer(peer_id, chat):
    message = get_news()
    answer(message, peer_id, chat)


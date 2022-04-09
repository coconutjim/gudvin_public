# -*- coding: utf-8 -*-
import json
import random

import requests

from apis.main.answer_util import answer
from log import log
from resources import breaking_news

NUM_NEWS = 9
MAX_WORDS = 3


def get_item_content(item):
    words = item.split()
    length = len(words)
    if length < 1:
        raise Exception('empty title')
    if length < MAX_WORDS + 1:
        return words[random.randint(0, length) - 1]
    res = ''
    num_words = random.randint(1, MAX_WORDS)
    ind = random.randint(0, length) - 1
    for i in range(0, num_words):
        res += words[(ind + i) % length] + ' '
    return res[:-1]


def get_news():
    log('getting news...')
    response = requests.get('https://meduza.io/api/v3/search?chrono=news&page=0&per_page=' + str(NUM_NEWS) +
                            '&locale=ru', verify=False)
    data = json.loads(response.text)['documents']
    if not data:
        raise Exception('no news found')
    news = list()
    i = 0
    for key in data:
        if i == NUM_NEWS:
            break
        news.append(data[key]['title'])
        i += 1
    random.shuffle(news)
    log('got news...')
    return news


def get_normal_news():
    news = get_news()
    res = breaking_news + '\n'
    i = 1
    for item in news:
        res += str(i) + '. ' + item + '\n'
        i += 1
    return res[:-1]


def get_random_news():
    news = get_news()
    log('shuffling news...')
    res = breaking_news + '\n'
    for item in news:
        res += get_item_content(item) + ' '
    res = res[:-1]
    log('shuffled news...')
    return res


def process_news_meduza_answer(rand, peer_id, chat):
    message = get_random_news() if rand else get_normal_news()
    answer(message, peer_id, chat)

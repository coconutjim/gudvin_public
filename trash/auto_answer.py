# -*- coding: utf-8 -*-
import requests
import json
import datetime

from log import log
from apis.main.answer_util import answer
from apis.main.vk_api import ACCESS_TOKEN


MINUTES_AUTO_ANSWER = 1200
TIME_TO_ANSWER = 1

ONLINE_MINUTES = 1800

auto_answer = u'Привет, я Гyдвин. К сожалению, Лев сейчас не может ответить (скорее всего, он спит), ' \
              u''u'но, возможно, я смогу вам помочь. Для того чтобы со мной связаться, достаточно ' \
              u''u'обратиться ко мне по имени. Чтобы понять, на что я способен, нужно написать ' \
              u'"Гyдвин, описание функций". И не стоит копипастить, не ленитесь. Я за этим слежу.'
copy_paste = u'Я же предупреждал. Копипастить не надо.'


def check_online():
    last_seen = get_last_seen()
    return (last_seen + datetime.timedelta(minutes=ONLINE_MINUTES)) > datetime.datetime.now()


def get_last_seen():
    method_url = 'https://api.vk.com/method/users.get?'
    data = dict(access_token=ACCESS_TOKEN, fields='last_seen')
    response = requests.post(method_url, data)
    return datetime.datetime.fromtimestamp(json.loads(response.text)['response'][0]['last_seen']['time'])


def process_command(message, online):
    body = message['body'].lower()
    chat = False
    peer_id = message['uid']
    if 'chat_id' in message:
        chat = True
        peer_id = message['chat_id']
    out = message['out']

    if body == u'гyдвин, описание функций':
        log('found copy-paste from ' + str(peer_id) + (' (chat)' if chat else ''))
        answer(copy_paste, peer_id, chat)
        return

    if u'гудвин' in body and u'автоответчик' in body:
        log('found auto answer request from ' + str(peer_id) + (' (chat)' if chat else ''))
        answer(auto_answer, peer_id, chat)
        return

    if not chat and out == 0 and message['read_state'] == 0:
        date = datetime.datetime.fromtimestamp(message['date'])
        now = datetime.datetime.now()
        if (date + datetime.timedelta(minutes=MINUTES_AUTO_ANSWER)) < now \
                or (not online and (date + datetime.timedelta(minutes=TIME_TO_ANSWER)) < now):
            log('found unread message from ' + str(peer_id))
            answer(auto_answer, peer_id, chat)

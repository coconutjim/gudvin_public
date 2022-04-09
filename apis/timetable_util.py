# -*- coding: utf-8 -*-
import datetime
import json

import requests

from apis.main.answer_util import answer
from log import log
from resources import no_lessons

GROUP_MOB = 5752
GROUP_URPO = 5753
GROUP_ELBI = 5660


def get_timetable(group_id):
    log('getting timetable...')
    prefix = u'Мобилки: ' if group_id == GROUP_MOB else (u'УРПО: ' if group_id == GROUP_URPO else '')
    date = datetime.date.today().strftime('%Y.%m.%d')
    url = 'https://www.hse.ru/api/timetable/lessons?fromdate=' + date + '&todate=' + date + '&groupoid=' + \
          str(group_id) + '&receiverType=3'
    response = requests.get(url)
    result = json.loads(response.text)
    log('got timetable...')
    if result['Count'] == 0:
        return prefix + no_lessons
    lessons = result['Lessons']
    res = '\n'
    for lesson in lessons:
        time = lesson['beginLesson'] + '-' + lesson['endLesson']
        disc = lesson['discipline']
        lecturer = lesson['lecturer']
        aud = lesson['auditorium']
        str_repr = prefix + time + ' ' + disc + ' ' + lecturer + ' ' + aud
        res += str_repr + '\n'
    return res[:-1]


def process_timetable_answer(urpo, mob, elbi, peer_id, chat):
    if urpo and mob:
        answer(get_timetable(GROUP_URPO) + '\n\n' + get_timetable(GROUP_MOB), peer_id, chat)
        return
    if urpo:
        answer(get_timetable(GROUP_URPO), peer_id, chat)
    if mob:
        answer(get_timetable(GROUP_MOB), peer_id, chat)
    if elbi:
        answer(get_timetable(GROUP_ELBI), peer_id, chat)


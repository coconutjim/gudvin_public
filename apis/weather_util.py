# -*- coding: utf-8 -*-
import json

import requests

from apis.main.answer_util import answer, img_answer
from log import log
from resources import no_weather

OPENWEATHERMAP_API_KEY = ''
MOSCOW_ID = '524901'

FALLOUT_URL = 'http://mini.s-shot.ru/1024x768/JPEG/400/Z100/?https%3A%2F%2Fyandex.ru%2Fpogoda%2Fmoscow%2Fnowcast'


def get_weather():
    log('getting weather...')
    method_url = 'http://api.openweathermap.org/data/2.5/weather?'
    params = dict(APPID=OPENWEATHERMAP_API_KEY, id=MOSCOW_ID, units='metric')
    response = requests.get(method_url, params=params)
    weather = json.loads(response.text)
    main = weather['main']
    res = u'\nПогoда в Москве: \n{}\u00b0 (от {}\u00b0 до {}\u00b0)\nВлажность: {}%\nДавление: {:.1f} мм рт. ст.\n' \
          u'Ветер: {} м/с, {}\u00b0\nОблачность: {}%'.format(main['temp'], main['temp_min'], main['temp_max'],
                                                             main['humidity'], int(main['pressure']) * 0.750062,
                                                             weather['wind']['speed'], weather['wind']['deg'],
                                                             weather['clouds']['all'])
    log('got weather...')
    return res


def process_weather_answer(peer_id, chat):
    try:
        weather = get_weather()
        img_answer(weather, FALLOUT_URL, peer_id, chat)
    except Exception as e:
        log(str(e), error=True)
        answer(no_weather, peer_id, chat)

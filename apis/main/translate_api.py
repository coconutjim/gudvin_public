# -*- coding: utf-8 -*-
import requests
import json

from log import log

YA_TRANSLATE_KEY = ''

DEFAULT_LANGUAGE = 'ru'
DEFAULT_TONE_LANGUAGE = 'en'


def get_languages():
    method_url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    data = dict(key=YA_TRANSLATE_KEY, ui=DEFAULT_LANGUAGE)
    response = requests.get(method_url, data)
    return json.loads(response.text)['langs']


def translate(text, lang):
    log('translating...')
    method_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    data = dict(key=YA_TRANSLATE_KEY, lang=lang, text=text)
    response = requests.post(method_url, data)
    translation = json.loads(response.text)['text'][0]
    log('translated...')
    return translation

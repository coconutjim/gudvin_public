# -*- coding: utf-8 -*-
import json

import requests

from apis.main.answer_util import answer
from apis.main.translate_api import translate, DEFAULT_TONE_LANGUAGE
from apis.main.vk_api import retrieve_message_texts
from log import log
from resources import no_messages_count

MICROSOFT_KEY_TA = ''

EMPTY_ALIAS = '#Empty message#'


def analyze_texts(texts):
    documents = []
    i = 0
    for text in texts:
        documents.append(dict(language='en', id=str(i), text=text))
        i += 1
    log('analyzing texts...')
    headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': MICROSOFT_KEY_TA}
    method_url = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment?'
    data = dict(documents=documents)
    response = requests.post(method_url, json.dumps(data), headers=headers)
    result = json.loads(response.text)
    log('analyzed texts...')
    res = []
    for document in result['documents']:
        res.append(document['score'])
    return res


def process_tone_analysis_answer(count, peer_id, chat):
    texts = retrieve_message_texts(count, peer_id, chat, skip_mes=2)
    if texts is None:
        answer(no_messages_count, peer_id, chat)
        return
    translated = []
    for text in texts:
        tr = translate(text, DEFAULT_TONE_LANGUAGE)
        translated.append(tr)
    analysis_result = analyze_texts(translated)
    res = u'Анализ тональности\n'
    i = 0
    mean = 0
    empties = 0
    for t in translated:
        res += '{}) {}'.format(i + 1, t)
        if t == EMPTY_ALIAS:
            empties += 1
        else:
            mean += analysis_result[i]
            res += '({0:.2f}%)'.format(analysis_result[i] * 100)
        res += '\n'
        i += 1
    if empties != count:
        res += u'Общая тональность: {0:.2f}%'.format(mean / (count - empties) * 100)
    answer(res, peer_id, chat, need_translation=False)

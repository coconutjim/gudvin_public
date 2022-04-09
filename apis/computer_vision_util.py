# -*- coding: utf-8 -*-
import json
import urllib.parse

import requests

from apis.main.answer_util import answer
from apis.main.vk_api import find_image_url
from apis.main.translate_api import translate
from log import log
from resources import no_image_attached, no_found_on_image

MICROSOFT_KEY_CV = ''
RESULT_OPTIONS = 'Categories,Tags,Description,Faces,ImageType,Color,Adult'


def get_image_description(img_url):
    log('getting image description...')
    params = urllib.parse.urlencode({
        'subscription-key': MICROSOFT_KEY_CV,
        'visualFeatures': RESULT_OPTIONS
        })
    headers = {'content-type': 'application/json'}
    method_url = 'http://api.projectoxford.ai/vision/v1.0/analyze?' + params
    img_data = dict(URL=img_url)
    response = requests.post(method_url, json.dumps(img_data), headers=headers)
    result = json.loads(response.text)
    print(response.text)
    if 'description' not in result:
        return no_found_on_image
    desc = result['description']
    if 'captions' not in desc:
        return no_found_on_image
    captions = desc['captions']
    if captions is None or len(captions) == 0:
        return no_found_on_image
    # res = ''
    # for c in captions:
    #    res += c['text'] + '\n'
    # log('got image description...')
    # return res[:-1]
    log('got image description...')
    return captions[0]['text']


def form_description(img_url):
    desc = get_image_description(img_url)
    if desc == no_found_on_image:
        return no_found_on_image
    return u'Это ' + translate(desc, 'ru') + ' (' + desc + ')'


def process_cv_answer(message, peer_id, chat):
    img_url = find_image_url(message, peer_id, chat)
    if img_url is None:
        answer(no_image_attached, peer_id, chat)
        return
    answer(form_description(img_url), peer_id, chat)

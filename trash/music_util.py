import json
import random

import requests

from apis.main.answer_util import answer, PROGRAM_SIGN
from apis.main.vk_api import ACCESS_TOKEN
from log import log
from resources import no_such_music


def get_audio_name(query):
    log('getting audio name...')
    method_url = 'https://api.vk.com/method/audio.search'
    data = dict(access_token=ACCESS_TOKEN, q=query)
    response = requests.post(method_url, data)
    result = json.loads(response.text)['response']
    if result[0] == 0:
        log('no audio "' + query + '" found')
        return None
    audio = result[random.randint(1, len(result) - 1)]
    log('got audio name...')
    return 'audio' + str(audio['owner_id']) + '_' + str(audio['aid'])


def send_audio(peer_id, chat, audio_name):
    log('sending audio...')
    data = dict(access_token=ACCESS_TOKEN, message=PROGRAM_SIGN, attachment=audio_name)
    if chat:
        data['chat_id'] = peer_id
    else:
        data['user_id'] = peer_id
    method_url = 'https://api.vk.com/method/messages.send?'
    requests.post(method_url, data)
    log('sent audio...')


def process_audio_answer(query, peer_id, chat):
    audio_name = get_audio_name(query)
    if audio_name is None:
        answer(no_such_music, peer_id, chat)
        return
    send_audio(peer_id, chat, audio_name)
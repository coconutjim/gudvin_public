import requests
import json
import random

from log import log
from apis.main.vk_api import ACCESS_TOKEN, COMMUNITY_ID, load_gif
from apis.main.answer_util import PROGRAM_SIGN
from resources import post_ready
from apis.gif_util import GIPHY_KEY

WORD_KEY = ''

MUSIC_COMMUNITY_IDS = ['34384434', '23995866', '24068829']
NUM_AUDIO = '50'
MAX_AUDIO_OFFSET = 5000


def random_word():
    log('getting random word...')
    response = requests.get('http://api.wordnik.com/v4/words.json/randomWord?api_key=' + WORD_KEY)
    log('got random word...')
    return json.loads(response.text)['word']


def get_gif_url(query):
    log('getting gifs...')
    url = 'http://api.giphy.com/v1/gifs/search?api_key=' + GIPHY_KEY + '&q=' + query
    response = requests.get(url)
    log('got gifs...')
    data = json.loads(response.text)['data']
    if not data:
        raise Exception('no gifs for word ' + query)
    res = list()
    for item in data:
        res.append(item['images']['fixed_height_small']['url'])
    return res[random.randint(0, len(res) - 1)]


def post_data(query, gif_name, target, peer_id, chat):
    peer_id = str(peer_id)
    target = str(target)
    message = PROGRAM_SIGN + ' ' + post_ready

    log('posting...')
    music_community_id = MUSIC_COMMUNITY_IDS[random.randint(0, len(MUSIC_COMMUNITY_IDS) - 1)]
    offs = str(random.randint(0, MAX_AUDIO_OFFSET))
    code = 'var a = API.audio.get({"owner_id":"-' + music_community_id + '","count":"' + NUM_AUDIO + \
           '","offset":"' + offs + '"})@.aid[1];'
    code += 'API.audio.add({"owner_id":"-' + music_community_id + '","group_id":"' + COMMUNITY_ID + \
            '","audio_id":a});'
    code += 'var at = "' + gif_name + ',audio-' + music_community_id + '_" + a;'
    code += 'var pid = API.wall.post({"owner_id":"' + str(target) + '","message":"' + query + \
            '","attachments":at});'
    peer_cred = '"chat_id":"' + peer_id + '"' if chat else '"user_id":"' + peer_id + '"'
    code += 'var post = "wall' + target + '_" + pid;'
    code += 'var mid = API.messages.send({' + peer_cred + ',"message":"' + message + '","attachment":post});'
    data = dict(access_token=ACCESS_TOKEN, code=code)
    requests.post('https://api.vk.com/method/execute?', data)
    log('posted...')


def process_content_answer(target, peer_id, chat):
    not_success = True
    try_count = 0
    while not_success:
        try:
            try_count += 1
            if try_count > 30:
                break
            query = random_word()
            gif_url = get_gif_url(query)
            gif_name = load_gif(gif_url)
            post_data(query, gif_name, target, peer_id, chat)
            not_success = False
        except Exception as e:
            log(str(e), error=True)
            continue

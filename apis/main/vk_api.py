import requests
import json
import random

from log import log


ACCESS_TOKEN = ''
COMMUNITY_ID = '126722923'

POSTING_IMAGE_TIMEOUT = 10
POSTING_GIF_TIMEOUT = 10
POSTING_VOICE_TIMEOUT = 10
MESSAGES_TO_FIND_IMAGE = 10


def get_dialogs():
    log('getting dialogs...')
    method_url = 'https://api.vk.com/method/messages.getDialogs?'
    data = dict(access_token=ACCESS_TOKEN, count='20', v=5.4)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    log('got dialogs...')
    return result['response']['items']


def send_message(message, peer_id, chat, attachment=None):
    data = dict(access_token=ACCESS_TOKEN, message=message, v=5.68)
    if attachment is not None:
        data['attachment'] = attachment
    if chat:
        data['chat_id'] = peer_id
    else:
        data['user_id'] = peer_id
    method_url = 'https://api.vk.com/method/messages.send?'
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])


def load_img(img_url):
    response = requests.get(img_url)
    img_data = response.content
    img = {'photo': ('img.jpg', img_data)}

    log('getting upload server for image...')
    method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    data = dict(access_token=ACCESS_TOKEN, gid=COMMUNITY_ID, v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    upload_url = result['response']['upload_url']
    log('got upload server...')

    log('posting image to server...')
    response = requests.post(upload_url, files=img, timeout=POSTING_IMAGE_TIMEOUT, data={'v': '3.0'})
    result = json.loads(response.text)
    log('posted image...')

    log('getting image name...')
    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    data = dict(access_token=ACCESS_TOKEN, gid=COMMUNITY_ID, photo=result['photo'], hash=result['hash'],
                server=result['server'], v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response'][0]
    img_name = '{}{}_{}'.format('photo', result['owner_id'], result['id'])
    log('got image name...')
    return img_name


def load_gif(gif_url):
    response = requests.get(gif_url)
    img_data = response.content
    img = {'file': ('img.gif', img_data)}

    log('getting upload server for gif..')
    method_url = 'https://api.vk.com/method/docs.getUploadServer?'
    data = dict(access_token=ACCESS_TOKEN, group_id=COMMUNITY_ID, v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    upload_url = result['response']['upload_url']
    log('got upload server..')
    log('posting gif to server')
    response = requests.post(upload_url, files=img, timeout=POSTING_GIF_TIMEOUT)
    result = json.loads(response.text)
    log('posted gif..')
    log('getting gif name..')
    method_url = 'https://api.vk.com/method/docs.save?'
    data = dict(access_token=ACCESS_TOKEN, file=result['file'], title='gif', v=5.78)
    response = requests.post(method_url, data)
    print(response.text)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response'][0]
    gif_name = '{}{}_{}'.format('doc', result['owner_id'], result['id'])
    log('got gif name..')
    return gif_name


def load_voice(data):
    voice = {'file': ('ans.mp3', data)}

    log('getting upload server for voice..')
    method_url = 'https://api.vk.com/method/docs.getUploadServer?'
    data = dict(access_token=ACCESS_TOKEN, type='audio_message', group_id=COMMUNITY_ID, v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    upload_url = result['response']['upload_url']
    log('got upload server..')

    log('posting voice to server')
    response = requests.post(upload_url, files=voice, timeout=POSTING_VOICE_TIMEOUT)
    result = json.loads(response.text)
    log('posted voice..')

    log('getting voice link..')
    method_url = 'https://api.vk.com/method/docs.save?'
    data = dict(access_token=ACCESS_TOKEN, file=result['file'], title='voice', v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response'][0]
    voice_name = '{}{}_{}'.format('doc', result['owner_id'], result['id'])
    log('got voice name..')
    return voice_name


def find_image_url(message, peer_id, chat):
    log('looking for image in current message...')
    image_url = get_image_url(message, sizes_types=False)
    if image_url is not None:
        return image_url
    log('looking for image in previous messages...')
    method_url = 'https://api.vk.com/method/messages.getHistory?'
    data = dict(access_token=ACCESS_TOKEN, count=MESSAGES_TO_FIND_IMAGE, v=5.78)
    if chat:
        data['chat_id'] = peer_id
    else:
        data['user_id'] = peer_id
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response']['items']
    if len(result) < 1:
        return None
    for mes in result:
        image_url = get_image_url(mes)
        if image_url is not None:
            return image_url


def get_image_url(message, sizes_types=True):
    log('getting image url...')
    if 'attachments' not in message:
        return None
    attachments = message['attachments']
    if attachments is None or len(attachments) == 0:
        return None
    image = None
    for a in attachments:
        if a['type'] == 'photo':
            image = get_max_image_size_url(a['photo'], sizes_types)
            break
    if image is not None:
        log('got image url...')
    return image


def get_max_image_size_url(sizes, sizes_types=True):
    if sizes_types:
        sizes = sizes['sizes']
        max_width = 0
        max_size = 0
        i = 0
        for size in sizes:
            if size['type'] in ['s', 'm', 'x', 'y', 'z', 'w']:
                if size['width'] > max_width:
                    max_width = size['width']
                    max_size = i
            i += 1
        return sizes[max_size]['url']
    if 'photo_1280' in sizes:
        return sizes['photo_1280']
    if 'photo_807' in sizes:
        return sizes['photo_807']
    if 'photo_604' in sizes:
        return sizes['photo_604']
    if 'photo_130' in sizes:
        return sizes['photo_130']
    if 'photo_75' in sizes:
        return sizes['photo_75']


def get_video_name(query):
    log('getting video name...')
    method_url = 'https://api.vk.com/method/video.search'
    data = dict(access_token=ACCESS_TOKEN, q=query, adult='1', v=5.78)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response']['items']
    if len(result) == 0:
        log('no video "' + query + '" found')
        return None
    video = result[random.randint(0, len(result) - 1)]
    video_name = 'video{}_{}'.format(video['owner_id'], video['id'])
    log('got video name...')
    return video_name


EMPTY_ALIAS = '#Empty message#'


def retrieve_message_texts(count, peer_id, chat, skip_mes=0):
    log('retrieving messages...')
    method_url = 'https://api.vk.com/method/messages.getHistory?'
    data = dict(access_token=ACCESS_TOKEN, count=(count + skip_mes), v=5.78)
    if chat:
        data['chat_id'] = peer_id
    else:
        data['user_id'] = peer_id
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    result = result['response']['items']
    if len(result) < (count + skip_mes):
        return None
    res = []
    for mes in result[skip_mes:]:
        text = mes['body']
        if 'FROM' in text and '(TG):' in text:
            text = text[(text.find('TG):') + 5):]
        if text == '':
            text = EMPTY_ALIAS
        res.append(text)
    log('retrieved messages...')
    return reversed(res)

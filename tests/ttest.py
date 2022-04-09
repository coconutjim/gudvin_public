# -*- coding: utf-8 -*-
__author__ = 'Lev'
import json
import datetime
import re

import requests
from requests_oauthlib import OAuth1
import urllib
import base64
import random

from log import log
# from apis.main.twitter_api import TWITTER_OAUTH
from apis.main.vk_api import ACCESS_TOKEN, COMMUNITY_ID
from apis.main.answer_util import PROGRAM_SIGN
from bs4 import BeautifulSoup as Soup
'''
data = dict(access_token=ACCESS_TOKEN, fields='last_seen')
resp = requests.post('https://api.vk.com/method/users.get?', data)
print resp.text
ls = json.loads(resp.text)['response'][0]['last_seen']['time']
print(ls)
print(datetime.datetime.fromtimestamp(ls))'''

subs_key = ''
img_url = 'http://s57.radikal.ru/i155/1106/99/ce6ea8062794.jpg'

'''
body = '{\'URL\': \'http://s57.radikal.ru/i155/1106/99/ce6ea8062794.jpg\'}'

# API request for Emotion Detection

headers = {
    'Content-type': 'application/json',
}

params = urllib.urlencode({
    'subscription-key': key,
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    print("Send request")
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
'''
'''
params = urllib.urlencode({
    'subscription-key': subs_key,
    'visualFeatures': 'Categories,Tags,Description,Faces,ImageType,Color,Adult'
})


img_data = dict(URL=img_url)
response = requests.post(method_url, json.dumps(img_data), headers=headers)
result = json.loads(response.text)
print[result]
print(result['captions'])
'''

'''
key = ''
text = 'dog cat'
lang = 'ru'
data = dict(key=key, lang=lang, text=text)
method_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
response = requests.post(method_url, data)
result = json.loads(response.text)['text'][0]
print(result)
'''

'''
domain = 'http://copout.me'
response = requests.get(domain)
soup = Soup(response.text, 'html.parser')
path = soup.find('a',  {'class': 'btn-generation btn-open-excuse'})['data-href']
link = domain + path
response = requests.get(link)
soup = Soup(response.text, 'html.parser')
text = soup.find('blockquote').text
print(text)
'''

'''
method_url = 'https://api.vk.com/method/messages.getHistory?'
data = dict(access_token=ACCESS_TOKEN, uid=12256121, count=10)
response = requests.post(method_url, data)
print(response.text)
result = json.loads(response.text)['response']
for m in result[1:]:
    print(m)
'''

'''
OLDEST_ADONEZH_ID = 286851644564594688
NEWEST_ADONEZH_ID = 771733213249204224

#method_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=radioadonezh&count=200&max_id=286851644564594688'
method_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
tweet_id = random.randint(OLDEST_ADONEZH_ID, NEWEST_ADONEZH_ID)
data = dict(screen_name='radioadonezh', count=1, max_id=971733213249204224, trim_user='true', include_rts='false')
response = requests.get(method_url, params=data, auth=TWITTER_OAUTH)
print response.text
result = json.loads(response.text)
text = result[0]['text']
print(text)
'''

'''
DOMAIN_URL = 'http://www.supertosty.ru'
WISHES_URL = 'http://www.supertosty.ru/pozhelaniya'
response = requests.get(WISHES_URL)
soup = Soup(response.text, 'html.parser')
categories = soup.find('ul', {'class': 'side_menu_link'}).find_all('li')
category = random.choice(categories).find('a')['href']
link = DOMAIN_URL + category
response = requests.get(link)
soup = Soup(response.text, 'html.parser')
wishes = soup.find('div', {'class': 'main_middle'}).find_all('div', {'class': 'tost_item'})
wish = random.choice(wishes).find('div').text
#wish = wish.replace('©', '')
wish = wish.encode('latin1').decode('cp1251').encode('utf8').replace('©', '')
print(wish)
'''


api_key = ''


'''
from StringIO import StringIO
from common import log

def load_gif(gif_url):
    #img_data = StringIO('ex.mp3')
    #img_data = open('ex.mp3', 'rb')
    img_data = gif_url
    img = {'file': ('ans.mp3', img_data)}

    log('getting upload server for gif..')
    method_url = 'https://api.vk.com/method/docs.getUploadServer?'
    data = dict(access_token=ACCESS_TOKEN, type='audio_message', v='5.38')
    response = requests.post(method_url, data)
    log(response.text)
    result = json.loads(response.text)
    upload_url = result['response']['upload_url']
    log('got upload server..')

    log('posting gif to server')
    response = requests.post(upload_url, files=img, timeout=10)
    log(response.text)
    result = json.loads(response.text)
    # log(result)
    log('posted gif..')

    log('getting gif link..')
    method_url = 'https://api.vk.com/method/docs.save?'
    data = dict(access_token=ACCESS_TOKEN, file=result['file'], title='gif')
    response = requests.post(method_url, data)
    log(response.text)
    result = json.loads(response.text)['response'][0]
    log('got gif link..')
    gif_name = 'doc' + str(result['owner_id']) + '_' + str(result['did'])
    return gif_name


def send_gif(peer_id, chat, gif_name):
    log('sending gif...')
    data = dict(access_token=ACCESS_TOKEN, message=PROGRAM_SIGN, attachment=gif_name)
    if chat:
        data['chat_id'] = peer_id
    else:
        data['user_id'] = peer_id
    method_url = 'https://api.vk.com/method/messages.send?'
    requests.post(method_url, data)
    log('sent gif...')

method_url = 'http://api.voicerss.org'
params = dict(key=api_key, hl='en-us', src='suka', f='48khz_16bit_stereo')
response = requests.get(method_url, params=params)
import io
print(response.text)
with open('tst.mp3', 'w') as file_:
    file_.write(response.text.encode("UTF-8"))
'''


'''
from voice_util import get_audio_data
data = get_audio_data('лол')
load_gif(data)
'''

#method_url = 'https://api.vk.com/method/docs.save?'
#data = dict(access_token=ACCESS_TOKEN, file='54685232|126722923|0|812234|7c4ec6a660|gif|126140|img.gif|9ffce75b91f06036abe57d165c76cc00|9cf38de83539f4d2c45361544bf6e50e|m_7c4ec6a660|28|m:130x98,s:100x75,o:133x100|W10=', title='gif', captcha_sid='118997550595', captcha_key='szvq')
#response = requests.post(method_url, data)
#log(response.text)


#method_url = 'https://api.vk.com/method/messages.send?'
#data = dict(user_id='54685232', access_token=ACCESS_TOKEN, message='lol', captcha_sid='420972519512', captcha_key='dsmk')
#response = requests.post(method_url, data)
#log(response.text)

#print(u''.join(WP_LINES[10]))

'''
log('getting gif link..')
method_url = 'https://api.vk.com/method/docs.save?'
data = dict(access_token=ACCESS_TOKEN, captcha_sid='601523328138', captcha_key='deekq', file='54685232|0|0|806228|3381799e6b|ogg|19443|ans.mp3|765df27d2f9685a37434c5cd539db09d|ca8b8cdea1d73645d6809869f8196f5d||||eyJhdWRpb19tc2ciOnsiZHVyYXRpb24iOjEuMTgsIndhdmVmb3JtIjoiMzI6MDAwMDAwMDAwMDAwM2NubzAxN2Z2ZjVhbGwyYXYxYm8wdjI5bDdzY2cyMjMxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAifX0=', title='gif')
response = requests.post(method_url, data)
log(response.text)
result = json.loads(response.text)['response'][0]
log('got gif link..')
gif_name = 'doc' + str(result['owner_id']) + '_' + str(result['did'])

s = u'лол китайский ыыы sds'
s1 = u'китайский'
s2 = u'тайский'
regex1 = r'\b' + s1 + r'\b'
regex2 = r'\b' + s2.encode('utf-8') + r'\b'
regex3 = r'\bsds\b'
print re.search(regex1, s, re.UNICODE)
print re.search(regex2, s.encode('utf-8'))
print regex1
print s
print re.search(regex3, s)
'''


import config
config.setup_config('config.ini', 'config_spec.ini')
print(config.config['Main']['alive'].__class__.__name__)




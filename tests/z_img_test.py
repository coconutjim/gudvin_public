__author__ = 'Lev'
import requests
import json

from apis.main.vk_api import ACCESS_TOKEN

'''
method_url = 'https://api.vk.com/method/video.search'
data = dict(access_token=ACCESS_TOKEN, q='sss')
response = requests.post(method_url, data)
result = json.loads(response.text)['response']
print(result)
'''
#data = dict(access_token=ACCESS_TOKEN, attachment='audio54685232_222572013', user_id='204765858')
#method_url = 'https://api.vk.com/method/messages.send?'
#res = requests.post(method_url, data)
#print(res.text)

access_token = ACCESS_TOKEN
user_id = '54685232'
audio = 'audio54685232_222572013'
data = dict(access_token=access_token, user_id=user_id, attachment=audio)
response = requests.post('https://api.vk.com/method/messages.send?', data)
print(response.text)
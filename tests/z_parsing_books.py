# -*- coding: utf-8 -*-
__author__ = 'Lev'
import requests
import json
import time
import codecs
import re

from apis.main.vk_api import ACCESS_TOKEN
from common import WP_PATH

PATTERN = re.compile('^– ([^–]*)')

WP_PATH2 = 'wp2p.txt'

COMMUNITY_ID = '-99126056'
MAX_COUNT_POST = 100
FILENAME = 'z_frazy.txt'

'''
method_url = 'https://api.vk.com/method/wall.get?'
posts_exist = True
i = 0
pc = 0
pp = 0
with codecs.open(FILENAME, "w", "utf-16") as f:
    while posts_exist:
        if i % 4 == 0:
            time.sleep(1)
        data = dict(access_token=ACCESS_TOKEN, owner_id=COMMUNITY_ID, count=str(MAX_COUNT_POST), offset=str(MAX_COUNT_POST * i))
        response = requests.post(method_url, data)
        posts = json.loads(response.text)['response']
        if len(posts) < 2:
            posts_exist = False
            break
        for post in posts[1:]:
            text = post['text']
            if len(text) > 0 and len(text) < 140:
                f.write(text + '\n')
                pp += 1
            pc += 1
        i += 1
        print(i)
print(pp)
print(pc)
'''

'''
with open('z_frazy_cens.txt') as f:
    un = []
    res = f.readlines()
    for s in res:
        if s not in un:
            un.append(s)
    print(len(res))
    print(len(un))
    with open('z_bydlo.txt', 'a') as f1:
        for s in un:
            f1.write(s)
'''

'''
with open(WP_PATH) as f:
    lines = f.readlines()
with open(WP_PATH2) as f:
    lines += f.readlines()
res = []
for line in lines:
    matches = PATTERN.match(line)
    if matches is not None:
        s = matches.group(1)
        if len(s) > 140 or len(s) < 1:
            continue
        if s.endswith(', '):
            s = s[:-2]
        res.append(s)
un = []
filename = 'z_wp.txt'
for s in res:
    if s not in un:
        un.append(s)
print(len(res))
print(len(un))
with open(filename, 'w') as f:
#with codecs.open(filename, "w", "utf-16") as f:
    for s in un:
        f.write(s + '\n')
'''
'''
rmk_path = 'rmk_orig.txt'

rmkp = re.compile('^– ([^–]*)')

res = []
with open(rmk_path) as f:
    lines = f.readlines()
    for line in lines:
        m = rmkp.match(line)
        if m is not None:
            s = m.group(1)
            if len(s) > 140 or len(s) < 1:
                continue
            if s.endswith(', '):
                s = s[:-2]
            res.append(s)
print(len(res))
un = []
filename = 'z_rmk.txt'
for s in res:
    if s not in un:
        un.append(s)
print(len(un))
with open(filename, 'w') as f:
    for s in un:
        f.write(s + '\n')
'''
'''
import common
with open(common.QUERIES_PATH, 'r') as f:
    with open('qq.txt', 'w') as f1:
        for s in f:
            f1.write(unicode(s, 'utf-8').capitalize().encode('utf-8'))
'''





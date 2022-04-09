# -*- coding: utf-8 -*-
import json
import random

import requests

from apis.main.answer_util import answer
from log import log
from resources import wiki_not_found


def get_wiki_definition(query):
    log('getting wiki definition...')
    method_url = 'https://ru.wikipedia.org/w/api.php?'
    params = dict(format='json', action='query', prop='extracts', redirects=1, exintro=1, explaintext=1, titles=query)
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)
    pages = result['query']['pages']
    log('got wiki definition...')
    if len(pages) == 1 and '-1' in pages:
        return None
    page = random.choice(list(pages.values()))
    text = page['extract']
    return text


def process_wiki_answer(query, peer_id, chat):
    definition = get_wiki_definition(query)
    if definition is None:
        definition = wiki_not_found
    answer(definition, peer_id, chat)

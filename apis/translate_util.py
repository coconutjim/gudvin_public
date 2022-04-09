# -*- coding: utf-8 -*-
import re

from log import log
import config
from apis.main.answer_util import answer, PROGRAM_SIGN
from apis.main.vk_api import retrieve_message_texts
from apis.main.translate_api import translate, DEFAULT_LANGUAGE
from resources import no_translate, no_messages_count, many_languages_trace

MAX_LANG_TRACE = 20


def parse_language(s):
    for k, v in config.languages.items():
        regex = r'\b' + v.lower() + r'\b'
        if k in s or re.search(regex, s, re.UNICODE):
            return k
    return None


def process_translate_answer(body, texts_count, peer_id, chat):
    lang = parse_language(body)
    if lang is None:
        lang = DEFAULT_LANGUAGE
    texts = retrieve_message_texts(texts_count, peer_id, chat, skip_mes=1)
    if texts is None:
        answer(no_messages_count, peer_id, chat)
        return
    translated = []
    try:
        for text in texts:
            tr = translate(text, lang)
            translated.append(tr)
    except Exception as e:
        log(str(e), error=True)
        answer(no_translate, peer_id, chat)
        return
    if len(translated) == 1:
        res = translated[0]
    else:
        i = 1
        res = u'\n'
        for t in translated:
            res += u'{}) {}\n'.format(i, t)
            i += 1
        res = res[:-1]
    answer(res, peer_id, chat, need_translation=False)


def process_translate_tracing_answer(ls, trace, peer_id, chat):
    ls = ls.split(' ')
    if len(ls) > MAX_LANG_TRACE:
        answer(many_languages_trace, peer_id, chat)
        return
    parsed = []
    for l in ls:
        lang = parse_language(l)
        if lang is None:
            answer(no_translate, peer_id, chat)
            return
        parsed.append(lang)
    texts = retrieve_message_texts(1, peer_id, chat, skip_mes=2)
    if texts is None:
        answer(no_translate, peer_id, chat)
        return
    text = list(texts)[0]
    if text is None or text == '' or text == PROGRAM_SIGN:
        answer(no_translate, peer_id, chat)
        return
    res = u'Трассировка с цепочкой:\n' if trace else u''
    i = 1
    try:
        for lang in parsed:
            text = translate(text, lang)
            if trace:
                res += u'{}) {} ({}, {})\n'.format(i, text, translate(text, DEFAULT_LANGUAGE),
                                                   config.languages[lang])
            i += 1
    except Exception as e:
        log(str(e), error=True)
        answer(no_translate, peer_id, chat)
        return
    if trace:
        res = res[:-1]
    else:
        res = text
    answer(res, peer_id, chat, need_translation=False)

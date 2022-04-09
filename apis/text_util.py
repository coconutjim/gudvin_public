# -*- coding: utf-8 -*-
import random

from apis.main.answer_util import answer
from log import log
from resources import no_text_message


def generate_message(lexicon):
    log('getting text...')
    lines_len = len(lexicon)
    if lines_len == 0:
        return no_text_message
    rand_index = random.randint(0, lines_len - 1)
    text = lexicon[rand_index]
    log('got text...')
    return text


def process_text_answer(lexicon, peer_id, chat):
    message = generate_message(lexicon)
    answer(message, peer_id, chat)

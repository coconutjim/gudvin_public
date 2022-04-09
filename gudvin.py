# -*- coding: utf-8 -*-
import re

import config
import resources
from log import log
from apis.main.answer_util import answer
from apis.translate_util import parse_language, process_translate_answer, process_translate_tracing_answer
from apis.computer_vision_util import process_cv_answer
from apis.excuse_util import process_excuse_answer
from apis.gif_util import process_gif_answer
from apis.img_desc_util import process_img_desc_answer
from apis.img_util import process_img_answer
from apis.news_util_adonezh import process_news_adonezh_answer
from apis.news_util_meduza import process_news_meduza_answer
from apis.text_util import process_text_answer
from apis.time_util import process_time_answer
from apis.timetable_util import process_timetable_answer
from apis.tone_analysis_util import process_tone_analysis_answer
from apis.video_util import process_video_answer
from apis.voice_util import process_voice_answer, process_voice_answer_query
from apis.weather_util import process_weather_answer
from apis.wiki_util import process_wiki_answer
from random import randint

SSE_PEER_ID = 132


def process_command(message):
    if 'chat_id' in message and message['chat_id'] == 156:
        return

    body = message['body'].lower()
    chat = False
    peer_id = message['user_id']
    if 'chat_id' in message:
        chat = True
        peer_id = message['chat_id']
    out = message['out']

    is_in_stop_list = peer_id in config.stop_peer_list

    triggered, finished = process_triggers(body, out, peer_id, chat)
    if finished:
        return

    if triggered and 'умри' in body and config.alive:
        log_request('turn to death', peer_id, chat)
        if out == 0:
            if not is_in_stop_list:
                answer(resources.not_allowed, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        config.alive = False
        return

    if triggered and 'живи' in body and out == 1 and not config.alive:
        log_request('turn to life', peer_id, chat)
        answer(prepare_ok_answer(out), peer_id, chat)
        config.alive = True
        return

    if not config.alive:
        return

    if 'гудвин он' in body and is_in_stop_list:
        log_request('turn on in chat', peer_id, chat)
        config.stop_peer_list.remove(peer_id)
        answer(prepare_ok_answer(out), peer_id, chat)
        return

    if 'гудвин офф' in body and not is_in_stop_list:
        log_request('turn off in chat', peer_id, chat)
        config.stop_peer_list.add(peer_id)
        answer(prepare_ok_answer(out), peer_id, chat)
        return

    if is_in_stop_list:
        return

    if 'гудвин офф' in body and not is_in_stop_list:
        log_request('turn off in chat', peer_id, chat)
        config.stop_peer_list.add(peer_id)
        answer(prepare_ok_answer(out), peer_id, chat)
        return

    if triggered and 'монетк' in body:
        log_request('coin', peer_id, chat)
        answer('Орёл' if randint(0, 9) == 1 else 'Решка', peer_id, chat)
        return

    if 'который час' in body or 'сколько времени' in body:
        log_request('time', peer_id, chat)
        process_time_answer(peer_id, chat)
        return

    if triggered and ('погода' in body or 'погоды' in body or 'погодой' in body or 'погоде' in body
                      or 'погоду' in body):
        log_request('weather', peer_id, chat)
        process_weather_answer(peer_id, chat)
        return

    if triggered and ('опис' in body or 'опиш' in body or 'список') and 'функц' in body:
        log_request('func description', peer_id, chat)
        answer(resources.func_description, peer_id, chat)
        return

    if triggered and 'смена интерфейса' in body:
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        if 'текст' in body:
            log_request('turn to text', peer_id, chat)
            config.answer_type = 'text'
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return
        if 'гифки' in body:
            log_request('turn to gif', peer_id, chat)
            config.answer_type = 'gif'
            answer(prepare_completing_answer(out), peer_id, chat)
            process_gif_answer(peer_id, chat)
            return
        if 'голос' in body:
            log_request('turn to voice', peer_id, chat)
            config.answer_type = 'voice'
            answer(prepare_completing_answer(out), peer_id, chat)
            process_voice_answer(config.lexicon, peer_id, chat)
            return

    if triggered and 'смена лексикона' in body:
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        if 'общий' in body:
            log_request('turn to all lexicon', peer_id, chat)
            config.lexicon = []
            config.lexicon += config.lexicon_wp
            config.lexicon += config.lexicon_bdl
            config.lexicon += config.lexicon_rmk
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return
        if 'быдло' in body:
            log_request('turn to bdl lexicon', peer_id, chat)
            config.lexicon = config.lexicon_bdl
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return
        if 'вим' in body:
            log_request('turn to wp lexicon', peer_id, chat)
            config.lexicon = config.lexicon_wp
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return
        if 'ремарк' in body:
            log_request('turn to rmk lexicon', peer_id, chat)
            config.lexicon = config.lexicon_rmk
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return
        if 'зыков' in body:
            log_request('turn to zyzy lexicon', peer_id, chat)
            config.lexicon = config.lexicon_zy
            answer(prepare_completing_answer(out), peer_id, chat)
            process_text_answer(config.lexicon, peer_id, chat)
            return

    if triggered and 'голос' in body and out == 1:
        log_request('voice', peer_id, chat)
        answer(resources.voice, peer_id, chat)
        return

    if triggered and ('поговори' in body or 'монолог' in body):
        log_request('mono', peer_id, chat)
        process_text_answer(config.lexicon, peer_id, chat)
        process_text_answer(config.lexicon, peer_id, chat)
        process_text_answer(config.lexicon, peer_id, chat)
        return

    if triggered and 'гифк' in body:
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('gif', peer_id, chat)
        process_gif_answer(peer_id, chat)
        return

    if triggered and 'картинк' in body and quotes_exists(body) and \
            ('опиш' in body or 'опис' in body or 'анализ' in body):
        if out == 0 and not config.images_allowed:
            answer(resources.images_not_allowed, peer_id, chat)
            return
        if out == 0 and not config.computer_vision_allowed:
            answer(resources.microsoft_services_not_allowed, peer_id, chat)
            return
        query = process_quotes(body)
        if query is None:
            answer(resources.bad_command, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('image with description', peer_id, chat)
        process_img_desc_answer(query, peer_id, chat)
        return

    if triggered and 'разреш' in body and 'картинк' in body:
        log_request('allow images', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.images_allowed = True
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if triggered and 'запрет' in body and 'картинк' in body:
        log_request('forbid images', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.images_allowed = False
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if triggered and 'картинк' in body and quotes_exists(body):
        if out == 0 and not config.images_allowed:
            answer(resources.images_not_allowed, peer_id, chat)
            return
        query = process_quotes(body)
        if query is None:
            answer(resources.bad_command, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('image', peer_id, chat)
        process_img_answer(query, peer_id, chat)
        return

    if triggered and 'музы' in body:
        log_request('music', peer_id, chat)
        answer(resources.no_music, peer_id, chat)
        return

    if triggered and 'видео' in body and quotes_exists(body):
        query = process_quotes(body)
        if query is None:
            answer(resources.bad_command, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('video', peer_id, chat)
        process_video_answer(query, peer_id, chat)
        return

    if triggered and 'скажи' in body and quotes_exists(body):
        text = process_quotes(body)
        if text is None:
            answer(resources.bad_command, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('say', peer_id, chat)
        process_voice_answer_query(text[0].encode('utf-8'), peer_id, chat)
        return

    if triggered and 'вики' in body and quotes_exists(body):
        text = process_quotes(body)
        if text is None:
            answer(resources.bad_command, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('wiki', peer_id, chat)
        process_wiki_answer(text.encode('utf-8'), peer_id, chat)
        return

    if triggered and 'разреш' in body and 'анализ' in body and 'картин' in body:
        log_request('allow cv', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.computer_vision_allowed = True
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if triggered and 'запрет' in body and 'анализ' in body and 'картин' in body:
        log_request('forbid cv', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.computer_vision_allowed = False
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if (triggered and 'картинк' in body and
            ('опиш' in body or 'опис' in body or 'анализ' in body)) or 'гак' in body:
        if out == 0 and not config.computer_vision_allowed:
            answer(resources.microsoft_services_not_allowed, peer_id, chat)
            return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('computer vision', peer_id, chat)
        process_cv_answer(message, peer_id, chat)
        return

    if triggered and 'треш' in body:
        log_request('news adonezh', peer_id, chat)
        process_news_adonezh_answer(peer_id, chat)
        return

    if triggered and 'новост' in body and 'нормал' in body:
        log_request('news meduza', peer_id, chat)
        process_news_meduza_answer(False, peer_id, chat)
        return
    if triggered and 'новост' in body:
        log_request('news meduza (random)', peer_id, chat)
        process_news_meduza_answer(True, peer_id, chat)
        return

    if triggered and 'разреш' in body and 'анализ' in body and 'тональност' in body:
        log_request('allow tone analysis', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.text_analysis_allowed = True
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if triggered and 'запрет' in body and 'анализ' in body and 'тональност' in body:
        log_request('forbid tone analysis', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return
        config.text_analysis_allowed = False
        answer(prepare_completed_answer(out), peer_id, chat)
        return
    if triggered and 'тональност' in body:
        if out == 0 and not config.text_analysis_allowed:
            answer(resources.microsoft_services_not_allowed, peer_id, chat)
            return
        texts_count = 1
        if quotes_exists(body):
            texts_count = process_quotes(body)
            if texts_count is None:
                answer(resources.bad_command, peer_id, chat)
                return
            if not texts_count.isdigit():
                answer(resources.bad_command, peer_id, chat)
                return
            texts_count = int(texts_count)
            if texts_count > 10:
                answer(resources.many_messages_count, peer_id, chat)
                return
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('tone analysis', peer_id, chat)
        process_tone_analysis_answer(texts_count, peer_id, chat)
        return

    if triggered and ('что' in body or ('о' in body and ('чем' in body or 'чём' in body))) \
            and 'дума' in body:
        log_request('query', peer_id, chat)
        process_text_answer(config.lexicon_queries, peer_id, chat)
        return

    if triggered and ('переведи' in body or 'перевод' in body):
        texts_count = 1
        if quotes_exists(body):
            texts_count = process_quotes(body)
            if texts_count is None or not texts_count.isdigit():
                answer(resources.bad_command, peer_id, chat)
                return
            texts_count = int(texts_count)
            if texts_count > 10:
                answer(resources.many_messages_count, peer_id, chat)
                return
        log_request('translate', peer_id, chat)
        process_translate_answer(body, texts_count, peer_id, chat)
        return
    if triggered and 'трассир' in body and quotes_exists(body):
        ls = process_quotes(body)
        if ls is None:
            answer(resources.bad_command, peer_id, chat)
            return
        trace = False
        if 'цеп' in body:
            trace = True
        answer(prepare_ok_answer(out), peer_id, chat)
        log_request('translate trace', peer_id, chat)
        process_translate_tracing_answer(ls, trace, peer_id, chat)
        return
    if triggered and 'языки' in body:
        log_request('languages', peer_id, chat)
        answer(config.languages_description, peer_id, chat)
        return
    if triggered and 'смен' in body and 'язык' in body:
        lang = parse_language(body)
        if lang is not None:
            log_request('language change', peer_id, chat)
            config.current_language = lang
            answer(prepare_completed_answer(out), peer_id, chat)
            return

    if triggered and 'текущий язык' in body:
        log_request('current language', peer_id, chat)
        answer(config.languages[config.current_language], peer_id, chat)
        return

    if triggered:
        log_request('common', peer_id, chat)
        if config.answer_type == 'text':
            process_text_answer(config.lexicon, peer_id, chat)
        if config.answer_type == 'gif':
            process_gif_answer(peer_id, chat)
        if config.answer_type == 'voice':
            process_voice_answer(config.lexicon, peer_id, chat)
        return

    if out == 1 and 'блин..' in body:
        log_request('excuse', peer_id, chat)
        process_excuse_answer(peer_id, chat)
        return

    if 'не погодится' in body:
        log_request('no weather', peer_id, chat)
        answer('Да, не погoдится', peer_id, chat)
        return


def process_triggers(body, out, peer_id, chat):
    triggered = False
    if out == 0 or (out == 1 and not body.startswith('gudvin')):
        if 'гудвин' in body or config.absolute_trigger:
            triggered = True
        if not triggered:
            for t in config.triggers:
                if t in body:
                    triggered = True
                    break
    if not config.alive:
        return triggered, False

    if triggered and 'убери' in body and 'абсолютный триггер' in body:
        log_request('absolute trigger removing', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return triggered, True
        if not config.absolute_trigger:
            answer(resources.no_trigger, peer_id, chat)
            return triggered, True
        config.absolute_trigger = False
        answer(prepare_completed_answer(out), peer_id, chat)
        return triggered, True
    if triggered and 'убери' in body and quotes_exists(body):
        log_request('trigger removing', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return triggered, True
        trigger = process_quotes(body)
        if trigger is None:
            answer(resources.bad_command, peer_id, chat)
            return triggered, True
        if trigger not in config.triggers:
            answer(resources.no_trigger, peer_id, chat)
            return triggered, True
        config.triggers.remove(trigger)
        answer(prepare_completed_answer(out), peer_id, chat)
        return triggered, True

    if triggered and 'абсолютный триггер' in body:
        log_request('absolute trigger adding', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return triggered, True
        if config.absolute_trigger:
            answer(resources.trigger_exists, peer_id, chat)
            return triggered, True
        config.absolute_trigger = True
        answer(prepare_completed_answer(out), peer_id, chat)
        return triggered, True
    if triggered and 'триггер' in body and quotes_exists(body):
        log_request('trigger adding', peer_id, chat)
        if out == 0:
            answer(resources.not_allowed, peer_id, chat)
            return triggered, True
        trigger = process_quotes(body)
        if trigger is None:
            answer(resources.bad_command, peer_id, chat)
            return triggered, True
        if trigger in config.triggers:
            answer(resources.trigger_exists, peer_id, chat)
            return triggered, True
        config.triggers.add(trigger)
        answer(prepare_completed_answer(out), peer_id, chat)
        return triggered, True

    if triggered and 'триггеры' in body:
        log_request('triggers', peer_id, chat)
        if len(config.triggers) == 0:
            res = resources.no_triggers
        else:
            res = '\n{}\n'.format(resources.now_triggers)
            if config.absolute_trigger:
                res += '{}\n'.format(resources.abs_trigger)
            for t in config.triggers:
                res += t + '\n'
            res = res[:-1]
        answer(res, peer_id, chat)
        return triggered, True
    return triggered, False


def prepare_ok_answer(out):
    return resources.ok_lev if out == 1 else resources.ok


def prepare_completing_answer(out):
    return resources.completing_lev if out == 1 else resources.completing


def prepare_completed_answer(out):
    return resources.completed_lev if out == 1 else resources.completed


def quotes_exists(body):
    return body.count('"') == 2


def process_quotes(body):
    found = re.findall('"([^"]*)"', body)
    if found is None or len(found) == 0 or found[0] == '':
        return None
    return found[0]


def log_request(r_type, peer_id, chat):
    log('found {} request from {}{}'.format(r_type, peer_id, (' (chat)' if chat else '')))

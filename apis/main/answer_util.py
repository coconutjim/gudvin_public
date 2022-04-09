from log import log
from apis.main import vk_api as vk
import config
from apis.main.translate_api import translate, DEFAULT_LANGUAGE


PROGRAM_SIGN = 'Gudvin:'


def answer(message, peer_id, chat, need_translation=True):
    log('answering...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(PROGRAM_SIGN + ' ' + message, peer_id, chat)
    log('answered...')


def quiet_answer(message, peer_id, chat, need_translation=True):
    log('answering quietly...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(message, peer_id, chat)
    log('answered quietly...')


def img_answer(message, img_url, peer_id, chat, need_translation=True):
    img_name = vk.load_img(img_url)
    log('sending img...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(PROGRAM_SIGN + ' ' + message, peer_id, chat, attachment=img_name)
    log('sent img...')


def gif_answer(message, gif_url, peer_id, chat, need_translation=True):
    gif_name = vk.load_gif(gif_url)
    log('sending gif...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(PROGRAM_SIGN + ' ' + message, peer_id, chat, attachment=gif_name)
    log('sent gif...')


def voice_answer(message, audio_data, peer_id, chat, need_translation=True):
    voice_name = vk.load_voice(audio_data)
    log('sending voice...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(PROGRAM_SIGN + ' ' + message, peer_id, chat, attachment=voice_name)
    log('sent voice...')


def video_answer(message, video_name, peer_id, chat, need_translation=True):
    log('sending video...')
    if message != '' and config.current_language != DEFAULT_LANGUAGE and need_translation:
        message = translate(message, config.current_language)
    vk.send_message(PROGRAM_SIGN + ' ' + message, peer_id, chat, attachment=video_name)
    log('sent video...')

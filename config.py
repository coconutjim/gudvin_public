# -*- coding: utf-8 -*-
import operator
from configobj import ConfigObj
from pathlib import Path

from log import log
from apis.main.translate_api import get_languages, DEFAULT_LANGUAGE
from apis.main.twitter_api import setup_twitter_connection

# See load_lexicon()
lexicon = []
lexicon_wp = []
lexicon_bdl = []
lexicon_rmk = []
lexicon_zy = []
lexicon_queries = []


# See setup_languages()
languages = dict()
current_language = ''
languages_description = ''


# config.ini
config = None
# Main
alive = True
triggers = {'триггер', '¯\_(ツ)_/¯'}
absolute_trigger = False
stop_peer_list = set()
black_peer_list = set()
# Communication
lexicon_type = 'all'
answer_type = 'text'
# Permissions
images_allowed = True
computer_vision_allowed = True
text_analysis_allowed = True


LEXICON_WP_PATH = 'lexicon/wp.txt'
LEXICON_BDL_PATH = 'lexicon/bydlo.txt'
LEXICON_RMK_PATH = 'lexicon/rmk.txt'
LEXICON_ZY_PATH = 'lexicon/zyzy.txt'
LEXICON_QUERIES_PATH = 'lexicon/queries.txt'

CONFIG_PATH = 'config.ini'


def load_lexicon():
    global lexicon
    global lexicon_bdl
    global lexicon_rmk
    global lexicon_wp
    global lexicon_zy
    global lexicon_queries
    log('loading wp..')
    with open(LEXICON_WP_PATH, encoding='utf-8') as f:
        lexicon_wp = f.readlines()
    log('loaded wp...')
    log('loading bdl..')
    with open(LEXICON_BDL_PATH, encoding='utf-8') as f:
        lexicon_bdl = f.readlines()
    log('loaded bdl...')
    log('loading rmk..')
    with open(LEXICON_RMK_PATH, encoding='utf-8') as f:
        lexicon_rmk = f.readlines()
    log('loaded rmk...')
    log('loading zy...')
    with open(LEXICON_ZY_PATH, encoding='utf-8') as f:
        lexicon_zy = f.readlines()
    log('loaded zy...')
    lexicon += lexicon_bdl
    lexicon += lexicon_wp
    lexicon += lexicon_rmk
    log('{} items in lexicon'.format(len(lexicon)))
    log('loading queries..')
    with open(LEXICON_QUERIES_PATH, encoding='utf-8') as f:
        lexicon_queries = f.readlines()
    log('loaded queries...')
    log('{} items in queries'.format(len(lexicon_queries)))


def setup_languages():
    global languages
    global current_language
    global languages_description
    languages = get_languages()
    current_language = DEFAULT_LANGUAGE
    sorted_l = sorted(languages.items(), key=operator.itemgetter(1))
    languages_description += '\nСписок поддерживаемых языков:\n'
    for l in sorted_l:
        languages_description += '{} - {}\n'.format(l[1], l[0])
    languages_description = languages_description[:-1]


def create_config(path):
    conf = ConfigObj(path, encoding='utf8')
    section_main = {
        'alive': True,
        'triggers': ['бля', 'сука', 'пизд', 'ху', 'еба'],
        'stop_peer_list': [24366356, 400775735],
        'black_peer_list': [202616407, 156, 157]
    }
    section_communication = {
        'lexicon_type': 'all',
        'answer_type': 'text'
    }
    section_permissions = {
        'images_allowed': True,
        'computer_vision_allowed': True,
        'text_analysis_allowed': True
    }
    conf['Main'] = section_main
    conf['Communication'] = section_communication
    conf['Permissions'] = section_permissions
    conf.write()


def setup_config(path, spec_path):
    global config
    file = Path(path)
    log('reading config file...')
    if not file.is_file():
        log('creating new config...')
        create_config(path)
        log('new config created...')

    config_spec = ConfigObj(spec_path, interpolation=False, list_values=False, _inspec=True)
    print(config_spec)
    config = ConfigObj(path, interpolation=True) # configspec=config_spec)
    log('read config file...')
    print(config)


def setup():
    load_lexicon()
    setup_languages()
    setup_twitter_connection()
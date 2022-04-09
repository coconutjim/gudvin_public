import apis.voicerss_tts as voicerss_tts
from apis.main.answer_util import answer, voice_answer
from log import log
from resources import voice_problems
from apis.text_util import generate_message

VOICERSS_KEY = ''


def get_audio_data(text):
    log('getting voice...')
    data = voicerss_tts.speech({
        'key': VOICERSS_KEY,
        'hl': 'ru-ru',
        'src': text,
        'r': '0',
        'c': 'mp3',
        'f': '44khz_16bit_stereo',
        'ssml': 'false',
        'b64': 'false'
    })
    log('got voice...')
    return data['response']


def _voice_answer(message, peer_id, chat):
    try:
        audio_data = get_audio_data(message)
        voice_answer('', audio_data, peer_id, chat)
    except Exception as e:
        log(str(e), error=True)
        answer(voice_problems, peer_id, chat)


def process_voice_answer(lexicon, peer_id, chat):
    _voice_answer(generate_message(lexicon), peer_id, chat)


def process_voice_answer_query(query, peer_id, chat):
    _voice_answer(query, peer_id, chat)

from apis.main.answer_util import answer, video_answer
from apis.main.vk_api import get_video_name
from resources import no_such_video


def process_video_answer(query, peer_id, chat):
    video_name = get_video_name(query)
    if video_name is None:
        answer(no_such_video, peer_id, chat)
        return
    video_answer('', video_name, peer_id, chat)

import apis.computer_vision_util as computer_vision_util
import apis.img_util as img_util
from apis.main.answer_util import answer, img_answer
from resources import images_ended


def process_img_desc_answer(query, peer_id, chat):
    img_url = img_util.get_img_url(query)
    if img_url is None:
        answer(images_ended, peer_id, chat)
        return
    img_answer('', img_url, peer_id, chat)
    answer(computer_vision_util.form_description(img_url), peer_id, chat)

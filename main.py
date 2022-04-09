import time

from log import log
from config import setup
from apis.news_util_adonezh import update_newest_id
from apis.main.vk_api import get_dialogs
from gudvin import process_command

TRY_COUNT = 3


def try_run_command(command, message):
    not_success = True
    try_count = 0
    while not_success:
        try:
            try_count += 1
            if try_count > TRY_COUNT:
                break
            command(message)
            not_success = False
        except Exception as e:
            # raise e
            log(str(e), error=True)
            continue


def check_dialogs():
    result = get_dialogs()
    for message in result:
        try_run_command(process_command, message)


def cycle_checking():
    while True:
        try:
            check_dialogs()
        except Exception as e:
            # raise e
            log(str(e), error=True)
        time.sleep(0.5)


if __name__ == '__main__':
    try:
        setup()
        update_newest_id()
        cycle_checking()
    except Exception as ex:
        # raise ex
        log(str(ex), error=True)

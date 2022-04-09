from datetime import datetime

ERRORS_PATH = 'error_log.txt'


def log(message, error=False):
    message = '{}: {}'.format(datetime.now(), message)
    if error:
        message = 'ERROR: {}\n'.format(message)
        with open(ERRORS_PATH, 'a') as f:
            f.write(message)
    print(message)

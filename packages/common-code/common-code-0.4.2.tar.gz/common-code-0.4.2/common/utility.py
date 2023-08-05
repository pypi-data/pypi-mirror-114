import time
from datetime import datetime

from common.response_param import Results


def dt_time():
    nnn = time.time() - 8 * 60 * 60
    dat = datetime.fromtimestamp(nnn)
    ttt = dat.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ttt


def dt_now_time():
    nnn = time.time()
    dat = datetime.fromtimestamp(nnn)
    ttt = dat.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ttt


def check_page_and_size(page, size):
    results = Results()
    try:
        page = int(page)
    except:
        results.describe = "'page must be int'"
    try:
        size = int(size)
    except:
        results.describe = "'size must be int'"
    if results.describe:
        return results, page, size
    else:
        return None, page, size


class CriticalError(Exception):
    pass

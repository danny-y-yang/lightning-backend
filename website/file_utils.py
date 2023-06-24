import datetime
import os

import time

_DEFAULT_FORMAT = "%Y-%m-%d %H:%M"
THOUGHT_ID_PREFIX = "thought_"
DELETED_PREFIX = "DELETED_"

def now_epoch():
    return int(time.time())

def epoch_to_str(epoch_seconds, fmt=_DEFAULT_FORMAT):
    return datetime.datetime.fromtimestamp(epoch_seconds).strftime(fmt)

def now_to_str(fmt=_DEFAULT_FORMAT):
    """
    Returns current datetime in provided format.
    """
    return datetime.datetime.fromtimestamp(now_epoch()).strftime(fmt)

def get_file_ctime(f_path, fmt=_DEFAULT_FORMAT):
    ctime = os.path.getctime(f_path)
    ctime_str = datetime.datetime.fromtimestamp(ctime).strftime(fmt)
    return ctime_str, ctime


def get_thought_id_from_abs_path(abs_path):
    """
    :param f_path: Absolute path of file
    :return: UUID of thought
    """
    # /a/b/c/thought_<uuid>.txt -> thought_<uuid>.txt
    f_name: str = abs_path.split("/")[-1]

    # get <uuid>.txt then trim the ".txt"
    return get_thought_id_from_f_name(f_name)


def get_thought_id_from_f_name(f_name):
    return f_name.split("_")[-1][:-4]

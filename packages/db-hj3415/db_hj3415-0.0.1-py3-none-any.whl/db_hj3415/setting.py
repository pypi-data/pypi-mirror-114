import os
import pickle
import platform

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)

DEF_MONGO_ADDR = 'mongodb://localhost:27017'
DEF_WIN_SQLITE3_PATH = 'C:\\_db'
DEF_LINUX_SQLITE3_PATH = '/home/hj3415/Stock/_db'

FILENAME = 'db_setting.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


def load() -> dict:
    """
    return  {'mongo': 주소..., 'sqlite3': 경로...}
    """
    try:
        with open(FULL_PATH, "rb") as fr:
            p_dict = pickle.load(fr)
            logger.info(p_dict)
            return p_dict
    except (EOFError, FileNotFoundError) as e:
        logger.error(e)
        set_default()
        # 새로 만든 파일을 다시 불러온다.
        with open(FULL_PATH, "rb") as fr:
            p_dict = pickle.load(fr)
            logger.info(p_dict)
            return p_dict


def chg_mongo_addr(addr: str) -> dict:
    if not addr.startswith('mongodb://'):
        raise ValueError(f'Invalid mongo address : {addr}')
    else:
        p_dict = load()
        p_dict['mongo'] = addr
        with open(FULL_PATH, "wb") as fw:
            pickle.dump(p_dict, fw)
        return load()


def chg_sqlite3_path(path: str) -> dict:
    p_dict = load()
    p_dict['sqlite3'] = path
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(p_dict, fw)
    return load()


def set_default() -> dict:
    pickle_dict = {'mongo': DEF_MONGO_ADDR, 'sqlite3': ''}
    if 'Windows' in platform.platform():
        pickle_dict['sqlite3'] = DEF_WIN_SQLITE3_PATH
    elif 'Linux' in platform.platform():
        pickle_dict['sqlite3'] = DEF_LINUX_SQLITE3_PATH
    else:
        raise
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(pickle_dict, fw)
    return pickle_dict

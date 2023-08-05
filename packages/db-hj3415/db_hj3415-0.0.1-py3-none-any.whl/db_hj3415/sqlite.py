# 파일명을 sqlite3.py로 하면 sqlite3 모듈과 이름이 중복되어 에러가 발생한다.

from setting import load as load_setting

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class Base:
    def __init__(self):
        self.sqlite3_path = load_setting()['sqlite3']
        # sqlite3 에 연결...
        # logger.info(f"__init__ set db : {self.db}\t col : {self.col}")
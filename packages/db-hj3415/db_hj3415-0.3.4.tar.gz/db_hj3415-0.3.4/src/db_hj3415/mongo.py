"""nfs mongodb manager

mongodb 를 manage 하는 클래스 모음
"""
import datetime
import math
import re
import pymongo
from pandas import DataFrame
from util_hj3415 import utils
from .setting import load as load_setting
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def chk_deactivate_mongo(func):
    """
    setting 모듈에서 mongo 주소 값이 ''인 경우
    데코레이션을 통해 해당 함수를 사용하지 못하도록 하는 데코함수
    """
    def wrapper(*args, **kwargs):
        addr = load_setting()['mongo']
        if addr == '' or addr is None:
            print('mongo db is deactivated..')
            return None
        else:
            return func(*args, **kwargs)
    return wrapper


class Base:
    def __init__(self, db, col):
        self.mongo_addr = load_setting()['mongo']

        # mongodb 에 연결
        if self.mongo_addr != '':
            self.client = pymongo.MongoClient(self.mongo_addr)
            self.db = db
            self.col = col
            logger.info(f"__init__ set db : {self.db}\tcol : {self.col}")
        else:
            print('mongo db is deactivated..')
            self.client = None
            self.db = None
            self.col = None

    # ======================Base 만 가지는 함수들 ===========================

    def get_status(self) -> tuple:
        """
        Returns:
            tuple: 현재 설정된 (db, col)을 반환한다.

        Examples:
            ('005930', 'c103재무상태표q')
        """
        return self.mongo_addr, self.db, self.col

    def chg_addr(self, addr: str):
        """

        현 클래스에서 참조하는 몽고디비 주소를 변경한다.

        Args:
            addr (str): mongodb://...로 시작하는 주소

        Note:
            setting 모듈을 통해 피클로 저장되는 세팅이 변하는 것이 아님
            전체 db 설정을 바꾸려면 setting.chg_mongo_addr()함수 사용할 것
        """
        if not addr.startswith('mongodb://'):
            raise ValueError(f'Invalid mongo address : {addr}')
        else:
            logger.info(f'Set addr : {self.mongo_addr} -> {addr}')
            self.mongo_addr = addr
            self.client = pymongo.MongoClient(addr)

    # ======================상속 클래스에서 재구성할 수 있는 함수들================
    # get 관련함수는 self 를 사용하나 drop 관련 함수를 신중을 위해 self 를 사용하지 않고 반드시 인자로 받는다.

    @staticmethod
    @chk_deactivate_mongo
    def get_all_db() -> list:
        client = pymongo.MongoClient(load_setting()['mongo'])
        return sorted(client.list_database_names())

    @staticmethod
    @chk_deactivate_mongo
    def drop_all_db():
        client = pymongo.MongoClient(load_setting()['mongo'])
        pre_db = Base.get_all_db()
        for db in pre_db:
            client.drop_database(db)
        post_db = Base.get_all_db()
        print(f"Drop all db..{len(pre_db)} -> {len(post_db)}")

    @staticmethod
    @chk_deactivate_mongo
    def drop_db(db: str):
        client = pymongo.MongoClient(load_setting()['mongo'])
        pre_db = Base.get_all_db()
        if db in pre_db:
            client.drop_database(db)
            post_db = Base.get_all_db()
            print(f"Drop {db}..{len(pre_db)} -> {len(post_db)}")
        else:
            raise ValueError(f'Invalid value : {db}')

    def get_all_col(self, db: str = '') -> list:
        if db == '':
            pass
        else:
            self.db = db
        return sorted(self.client[self.db].list_collection_names())

    def drop_all_col(self, db: str):
        pre_cols = self.get_all_col(db)
        for col in pre_cols:
            self.client[db].drop_collection(col)
        post_db = self.get_all_col(db)
        print(f"Drop all col in {db}..{len(pre_cols)} -> {len(post_db)}")

    def drop_col(self, db: str, col: str):
        pre_cols = self.get_all_col(db)
        if col in pre_cols:
            self.client[db].drop_collection(col)
            post_cols = self.get_all_col()
            print(f"Drop {col} col in {db}..{pre_cols} -> {post_cols}")
        else:
            raise ValueError(f'Invalid value : {col}')

    def get_all_doc(self, db: str = '', col: str = '', rm_id=True) -> list:
        if db == '':
            pass
        else:
            self.db = db

        if col == '':
            pass
        else:
            self.col = col

        items = []
        if rm_id:
            for doc in self.client[self.db][self.col].find({}):
                del doc['_id']
                items.append(doc)
        else:
            items = list(self.client[self.db][self.col].find({}))
        return items


class MI(Base):
    """

    mi 데이터베이스 클래스

    Note:
        <<데이터베이스 구조>>\n
        데이터베이스 - mi\n
        컬렉션 -\n
        'aud', 'chf', 'gbond3y',\n
        'gold', 'silver', 'kosdaq',\n
        'kospi', 'sp500', 'usdkrw',\n
        'wti', 'avgper', 'yieldgap',\n
        'usdidx' - 총 13개\n
        도큐멘트 - date, value\n
    """
    COL_TITLE = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
                 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def __init__(self, index='kospi'):
        if index in self.COL_TITLE:
            super().__init__(db='mi', col=index)
        else:
            raise ValueError(f'Invalid value : {index}({self.COL_TITLE})')

    # ======================MI 만 가지는 함수들 ===========================

    def chg_index(self, index: str):
        if index in self.COL_TITLE:
            logger.info(f'Set col : {self.col} -> {index}')
            self.col = index
        else:
            raise Exception(f'Invalid value : {index}({self.COL_TITLE})')

    # ======================부모 클래스에서 재구성한 함수들================

    def get_all_indexes(self):
        return super().get_all_col()

    def drop_all_indexes(self):
        super().drop_all_col(db='mi')

    def drop_index(self, index: str):
        if index in self.COL_TITLE:
            self.drop_col(db='mi', col=index)
        else:
            raise Exception(f'Invalid value : {index}({self.COL_TITLE})')

    def get_all_item(self, index: str = '') -> list:
        if index == '':
            pass
        else:
            self.chg_index(index=index)
        return super().get_all_doc()

    # ========================특정 페이지 관련 함수들=======================

    def get_recent(self, index: str = '') -> dict:
        """
        저장된 가장 최근의 값을 반환하는 함수

        Args:
            index (str, optional): 13개의 컬렉션.

        Returns:
            dict: ex - {'date': '2021.07.26', 'value': '1047.63'}
        """
        if index == '':
            pass
        else:
            self.chg_index(index=index)

        d = self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
        del d['_id']
        return d

    def save(self, mi_dict: dict, index: str = '') -> bool:
        """

        Args:
            mi_dict (dict): ex - {'date': '2021.07.21', 'value': '1154.50'}
            index (str, optional): 13개의 컬렉션.
        """
        if index != '':
            self.chg_index(index=index)
        self.client[self.db][self.col].delete_many({'date': {"$eq": mi_dict['date']}})
        result = self.client[self.db][self.col].insert_one(mi_dict)
        return result.acknowledged


class Corps(Base):
    """

    mongodb에 저장된 재무데이터를 가져오는 클래스

    Note:
    <<구조>>\n
        데이터베이스 - 6자리 코드명\n
        컬렉션 -\n
        c101, c106, c108, dart\n
        c103손익계산서qy,\n
        c103재무상태표qy,\n
        c103현금흐름표qy,\n
        c104qy,\n
        도큐멘트참고\n
        - c106은 q와 y의 2개의 도큐먼트로 구성\n
        - c104는 중복되는 항목이 없어 2개의 페이지로 나눔\n
        - c103는 중복되는 항목이 있어 6개의 페이지로 나눔\n
    """
    COL_TITLE = ('c101', 'c104y', 'c104q', 'c106', 'c108',
                 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y', 'dart')

    def __init__(self, code: str, page='c101'):
        if utils.is_6digit(code) and page in self.COL_TITLE:
            self.code = code
            self.page = page
            super().__init__(db=code, col=page)
        else:
            raise ValueError(f'Invalid value : {code}(6 digit) / {page}({self.COL_TITLE})')

    # ======================Corps 만 가지는 함수들 ===========================

    def chg_code(self, code: str):
        """
        code 가 6자리 숫자인지 확인 후 세팅
        """
        if utils.is_6digit(code):
            logger.info(f'Set db : {self.db} -> {code}')
            self.code = code
            self.db = code
        else:
            raise ValueError(f'Invalid value : {code}(6 digit)')

    def chg_page(self, page: str):
        """
        page 가 COL_TITLE 인지 확인 후 세팅

        Note:
            <COL_TITLE>\n
            'c101', 'c104y', 'c104q',\n
            'c106', 'c108', 'dart',\n
            'c103손익계산서qy',\n
            'c103재무상태표qy',\n
            'c103현금흐름표qy',\n
        """
        if page in self.COL_TITLE:
            logger.info(f'Set col : {self.col} -> {page}')
            self.col = page
            self.page = page
        else:
            raise ValueError(f'Invalid col name : {page}({self.COL_TITLE})')

    # ======================부모 클래스에서 재구성한 함수들================

    @staticmethod
    def get_all_corps() -> list:
        return_list = []
        for col in Base.get_all_db():
            if utils.is_6digit(col):
                return_list.append(col)
        return sorted(return_list)

    @staticmethod
    def drop_all_corps():
        client = pymongo.MongoClient(load_setting()['mongo'])
        pre_db = Corps.get_all_corps()
        for db in pre_db:
            client.drop_database(db)
        post_db = Corps.get_all_corps()
        print(f"Drop all corps..{len(pre_db)} -> {len(post_db)}")

    @staticmethod
    def drop_corp(code: str):
        if utils.is_6digit(code):
            Base.drop_db(db=code)
        else:
            raise ValueError(f'Invalid value : {code}(6 digit)')

    def get_all_pages(self, code: str = '') -> list:
        if code == '':
            pass
        else:
            self.chg_code(code=code)
        return super().get_all_col()

    def drop_all_pages(self, code: str):
        if utils.is_6digit(code):
            super().drop_all_col(db=code)
        else:
            raise ValueError(f'Invalid value : {code}(6 digit)')

    def drop_page(self, code: str, page: str):
        if utils.is_6digit(code) and page in self.COL_TITLE:
            super().drop_col(db=code, col=page)
        else:
            raise ValueError(f'Invalid value : {code}(6 digit) {page}({self.COL_TITLE})')

    def get_all_item(self, code: str = '', page: str = '') -> list:
        if code == '':
            pass
        else:
            self.chg_code(code=code)
        if page == '':
            pass
        else:
            self.chg_page(page=page)
        return super().get_all_doc()


class C101(Corps):
    def __init__(self, code: str):
        super().__init__(code=code, page='c101')

    # ========================특정 페이지 관련 함수들=======================

    def save(self, c101_dict: dict) -> bool:
        """

        c101의 구조에 맞는 딕셔너리값을 받아서 구조가 맞는지 확인하고 맞으면 저장한다.

        Note:
            <c101_struc>\n
            'date', '코드', '종목명',\n
            '업종', '주가', '거래량',\n
            'EPS', 'BPS', 'PER',\n
            '업종PER', 'PBR', '배당수익률',\n
            '최고52주', '최저52주', '거래대금',\n
            '시가총액', '베타52주', '발행주식',\n
            '유통비율', 'intro'\n
        """
        c101_struc = ['date', '코드', '종목명', '업종', '주가', '거래량', 'EPS', 'BPS', 'PER', '업종PER', 'PBR', '배당수익률',
                      '최고52주', '최저52주', '거래대금', '시가총액', '베타52주', '발행주식', '유통비율', 'intro']
        # 리스트 비교하기
        # reference from https://codetorial.net/tips_and_examples/compare_two_lists.html
        if c101_dict['코드'] != self.db:
            raise ValueError("Code isn't equal input data and db data..")
        if sorted(c101_struc) == sorted(c101_dict.keys()):
            # 스크랩한 날짜이후의 데이터는 조회해서 먼저 삭제한다.
            query = {'date': {"$gte": c101_dict['date']}}
            self.client[self.db][self.col].delete_many(query)
            result = self.client[self.db][self.col].insert_one(c101_dict)
            return result.acknowledged
        else:
            raise ValueError('Invalid c101 dictionary structure..')

    def find(self, date: str) -> dict:
        """

        해당 날짜의 데이터를 반환한다.

        Args:
            date (str): 예 - 20201011(6자리숫자)
        """
        p = re.compile('^20[0-9][0-9][0,1][0-9][0-3][0-9]$')
        if p.match(date) is None:
            raise ValueError(f'Invalid date format : {date}(ex-20201011(6자리숫자))')
        else:
            converted_date = date[:4] + '.' + date[4:6] + '.' + date[6:]
        try:
            d = self.client[self.db][self.col].find({'date': converted_date}).next()
            del d['_id']
        except StopIteration:
            d = None
        return d

    def get_all(self) -> list:
        """

        저장된 모든 데이터를 딕셔너리로 가져와서 리스트로 포장하여 반환한다.
        """
        items = []
        for doc in self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> dict:
        """

        저장된 데이터에서 가장 최근 날짜의 딕셔너리를 반환한다.

        """
        d = self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
        del d['_id']
        return d


class C108(Corps):
    def __init__(self, code: str):
        super().__init__(code=code, page='c108')

    # ========================특정 페이지 관련 함수들=======================

    def get_all(self) -> list:
        """

        저장된 모든 데이터를 딕셔너리로 가져와서 리스트로 포장하여 반환한다.
        """
        items = []
        for doc in self.client[self.db][self.col].find({'날짜': {'$exists': True}}).sort('날짜', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> list:
        """

        저장된 데이터에서 가장 최근 날짜의 딕셔너리를 가져와서 리스트로 포장하여 반환한다.

        Returns:
            list: 한 날짜에 c108 딕셔너리가 여러개 일수 있어서 리스트로 반환한다.
        """
        # 저장되어 있는 데이터베이스의 최근 날짜를 찾는다.
        try:
            r_date = self.client[self.db][self.col].find({'날짜': {'$exists': True}}).sort('날짜', pymongo.DESCENDING).next()['날짜']
        except StopIteration:
            # 날짜에 해당하는 데이터가 없는 경우
            return []

        # 찾은 날짜를 바탕으로 데이터를 검색하여 리스트로 반환한다.
        r_list = []
        for r_c108 in self.client[self.db][self.col].find({'날짜': {'$eq': r_date}}):
            del r_c108['_id']
            r_list.append(r_c108)
        return r_list

    def save(self, c108_list: list) -> bool:
        """

        Args:
            c108_list (list): c108로 저장할 리스트 형식
        Note:
            c108_list 구조\n
            [{'날짜': '21/07/19', '제목': '...',\n
            '작성자': '...', '제공처': '...', \n
            '투자의견': '...', '목표가': '95,000',\n
            '내용': '...'},]\n
        """
        c108_list.append({'stamp': datetime.datetime.now()})  # c108가 리스트라서 append 사용
        # delete all documents in a collection
        self.client[self.db][self.col].delete_many({})
        result = self.client[self.db][self.col].insert_many(c108_list)
        return result.acknowledged


class C106(Corps):
    """

    Note:
        내부적으로 c106 단일컬렉션에\n
        title : c106y/q를 가지는\n
        2개의 도큐먼트로 구성됨.\n
    """
    PERIOD = ['q', 'y']

    def __init__(self, code: str, page: str = 'c106y'):
        """

         Args:
            code (str): 종목코드(디비명)
            page (str): c106y, c106q
        """
        if page[:4] == 'c106' and page[4:5] in self.PERIOD:
            super().__init__(code=code, page='c106')
            self.page = page
        else:
            raise ValueError(f'Invalid page : {page}(c106q or c106y)')

    # ======================부모 클래스에서 재구성한 함수들================

    def chg_page(self, page: str):
        # 실제로 c106에서는 페이지가 바뀌는 것이 아니라 도큐먼트가 바뀌는 것임
        col = page[:4]
        period = page[4:5]
        if col == 'c106' and period in self.PERIOD:
            self.page = period
        else:
            raise ValueError(f'Invalid page : {page}(c106q or c106y)')

    def get_all(self) -> dict:
        c106_dict = self.client[self.db][self.col].find_one({'title': self.page})
        del c106_dict['_id']
        del c106_dict['title']
        del c106_dict['stamp']
        return c106_dict

    # ========================특정 페이지 관련 함수들=======================

    def find(self, title: str) -> dict:
        page_dict = self.get_all()
        if page_dict is None:
            return {}
        else:
            return page_dict[title]

    def get_stamp(self) -> datetime.datetime:
        return self.client[self.db][self.col].find_one({'title': self.page})['stamp']

    def save(self, c106_dict: dict) -> bool:
        """

        Args:
            c106_dict (dict): c106으로 저장할 딕셔너리 형식

        Example:
            c106_dict 구조\n
            {'전일종가': {'동화약품': '14600'..., '노바렉스': '27900'},\n
            '시가총액': {'동화약품': '4078.0'..., '노바렉스': '4606.6'}}\n

        Note:
            각 항목이 중복되지 않는 경우라서 항목을 키로하는 딕셔너리를 인자로 받는다.
        """
        c106_dict['title'] = self.page
        c106_dict['stamp'] = datetime.datetime.now()
        # delete all documents in a collection
        self.client[self.db][self.col].delete_one({'title': self.page})
        result = self.client[self.db][self.col].insert_one(c106_dict)
        return result.acknowledged


class C1034(Corps):

    # ======================부모 클래스에서 재구성한 함수들================

    def get_all_title(self) -> list:
        """

        중복된 타이틀을 취급하지 않기 위해 타이틀 전체에서 중복된 타이틀을 제거하고 나머지 타이틀 리스트를 반환한다.

        Returns:
            list: 중복된 항목을 제외한 모든 항목을 담은 리스트
        """
        # 항목만 추출한 리스트 만들기
        title_list = []
        for item_dict in self.get_all_item():
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                pass
            else:
                title_list.append(item_dict['항목'])

        # 리스트 중복요소 찾기
        # https://infinitt.tistory.com/78
        count = {}
        for i in title_list:
            try:
                count[i] += 1
            except KeyError:
                count[i] = 1

        # 중복되지 않는 타이틀만으로 리스트를 만들어 반환하기
        return_list = []
        for k, v in count.items():
            if v == 1:
                return_list.append(k)

        return return_list

    def get_all(self) -> dict:
        """

        페이지의 모든 항목에 대한 값을 딕셔너리 형태로 반환.

        Returns:
            dict: 각 항목을 키로하고 해당 기간별 데이터를 값으로 하는 딕셔너리

        Example:
            리턴값 예시\n
            {'*(비지배)당기순이익': {...'2020/12': 1860.0, '2021/12': nan},
            '*(지배)당기순이익': {...'2020/12': 16021.5,'2021/12': nan},}

        """
        c1034_list = self.get_all_item()
        # c104_list 내부에서는 항목, 전년/분기대비, 년/월을 포함하는 딕셔너리가 담겨있다.
        return_dict = {}
        not_duplicated_titles = self.get_all_title()
        for item_dict in c1034_list:
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                continue
            if item_dict['항목'] in not_duplicated_titles:
                # 중복된 타이틀을 뺀 나머지 항목들은 타이틀을 키로 하고 년/월을 값으로 하는 새로운 딕셔너리로 만든다.
                temp_dict = {}
                # 전년/분기대비 타이틀 제거를 위해 새로운 임시 딕셔너리를 만든다.
                for k, v in item_dict.items():
                    if k.startswith('전') or k.startswith('항'):
                        pass
                    else:
                        temp_dict[k] = v

                if item_dict['항목'] in return_dict.keys():
                    raise KeyError(f"중복된 항목이 있음 : {item_dict['항목']}")
                else:
                    return_dict[item_dict['항목']] = temp_dict
        return return_dict

    def get_all_cmp(self) -> dict:
        """

        페이지의 모든 항목에 대한 전년/분기대비 값을 딕셔너리 형태로 반환.

        Returns:
            dict: 각 항목을 키로하고 전분기/년대비 증감 데이터를 값으로 하는 딕셔너리

        Example:
            리턴값 예시\n
            {'*(비지배)당기순이익': 26.1,
            '*(지배)당기순이익': -12.7,
            '*CAPEX': 8.0}

        """
        c1034_list = self.get_all_item()
        # c104_list 내부에서는 항목, 전년/분기대비, 년/월을 포함하는 딕셔너리가 담겨있다.
        return_dict = {}
        not_duplicated_titles = self.get_all_title()
        for item_dict in c1034_list:
            if 'stamp' in item_dict:
                # stamp 는 넘어가고...
                continue
            if item_dict['항목'] in not_duplicated_titles:
                temp_dict = {}
                for k, v in item_dict.items():
                    if k.startswith('전'):
                        temp_dict[k] = v
                # temp_dict 에는 {'전년대비': -1.36, '전년대비1': nan} 또는 {'전분기대비': 14.63} 가 담긴다.
                if len(temp_dict) == 1:
                    # {'전분기대비': 14.63}인 경우 ...
                    return_dict[item_dict['항목']] = temp_dict.popitem()[1]
                elif len(temp_dict) == 2:
                    # {'전년대비': -1.36, '전년대비1': nan}인 경우 ...
                    v = temp_dict.pop('전년대비1')
                    if math.isnan(v):
                        return_dict[item_dict['항목']] = temp_dict.pop('전년대비')
                    else:
                        return_dict[item_dict['항목']] = v
                else:
                    # 데이터가 없는 경우는 nan 으로 세팅한다.
                    return_dict[item_dict['항목']] = float('nan')
        return return_dict

    # ========================특정 페이지 관련 함수들=======================

    def get_stamp(self) -> datetime.datetime:
        return self.client[self.db][self.col].find({'stamp': {'$exists': True}}).next()['stamp']

    def find_cmp(self, title:str) -> float:
        """
        타이틀에 해당하는 전년/분기대비 값을 반환한다.
        *** 중복되는 title은 취급하지 않기로함...get_all_title()함수에서 정리함.
        """
        try:
            return self.get_all_cmp()[title]
        except KeyError:
            return float('nan')

    def find(self, title: str) -> dict:
        """
        타이틀에 해당하는 년도, 분기 딕셔너리를 반환한다.
        *** 중복되는 title은 취급하지 않기로함...get_all_title()함수에서 정리함.
        """
        try:
            return self.get_all()[title]
        except KeyError:
            return {}

    def sum_recent_4q(self, title: str) -> tuple:
        """
        c103q 또는 c104q 한정 해당 타이틀의 최근 4분기의 합을 (계산된 4분기 중 최근분기, 총합)의 튜플형식으로 반환한다.
        """
        if self.col.endswith('q'):
            # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
            # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
            od_q = OrderedDict(sorted(self.find(title=title).items(), reverse=False))
            logger.info(f'{title} : {od_q}')
            if len(od_q) < 4:
                # od_q의 값이 4개 이하이면 그냥 최근 연도의 값으로 반환한다.
                return C1034(code=self.db, page=self.col[:-1]+'y').latest_value(title=title)
            else:
                q_sum = 0
                last_date = list(od_q.items())[-1][0]
                for i in range(4):
                    # last = True 이면 최근의 값부터 꺼낸다.
                    d, v = od_q.popitem(last=True)
                    logger.debug(f'd:{d} v:{v}')
                    q_sum += 0 if math.isnan(v) else v
                return last_date, round(q_sum, 2)

        else:
            raise TypeError(f'Not support year data..{self.col}')

    def latest_value(self, title: str) -> tuple:
        """
        title 에 해당하는 가장 최근의 값을 ('2020/09', 39617.5)와 같은 튜플로 반환한다.
        만약 값이 nan 이면 바로 직전 것을 한번만 더 찾아 본다.
        """
        # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
        # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
        od = OrderedDict(sorted(self.find(title=title).items(), reverse=False))
        logger.info(f'{title} : {od}')
        try:
            last_one = od.popitem(last=True)
        except KeyError:
            # when dictionary is empty
            return None, 0
        logger.info(f'last_one : {last_one}')
        if isinstance(last_one[1], str):
            # last_one : ('Unnamed: 1', '데이터가 없습니다.') 인 경우
            return None, 0
        elif math.isnan(last_one[1]):
            last_one = od.popitem(last=True)
            if last_one is None:
                return None, 0
        return tuple(last_one)


class C104(C1034):
    """C104 컬렉션 관련 클래스
    """
    def __init__(self, code: str, page: str = 'c104y'):
        """

        Args:
            code (str): 종목코드(디비명)
            page (str): c104y, c104q(컬렉션명)
        """
        super().__init__(code=code, page=page)

    def save(self, c104_list: list) -> bool:
        """데이터베이스에 저장

        c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에
        stamp 를 검사하여 12시간 전보다 이전에 저장된 자료가 있으면
        삭제한 후 저장하고 12시간 이내의 자료는 삭제하지 않고
        데이터를 추가하는 형식으로 저장한다.

        Args:
            c104_list (list): 딕셔너리를 담은 리스트 형식

        Returns:
            bool: 저장 성공 실패 여부

        Example:
            c104_list 예시\n
            [{'항목': '매출액증가율',...'2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율',...'2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        time_now = datetime.datetime.now()
        # c104가 리스트라서 append 사용
        c104_list.append({'stamp': time_now})
        if self.client[self.db][self.col].find_one({'stamp': {'$lt': time_now - datetime.timedelta(days=.5)}}):
            # delete all documents in a collection
            self.client[self.db][self.col].delete_many({})
        result = self.client[self.db][self.col].insert_many(c104_list)
        return result.acknowledged


class C103(C1034):
    """C103 컬렉션 관련 클래스
    """
    def __init__(self, code: str, page: str = 'c103재무상태표y'):
        """

        Args:
            code (str): 종목코드(디비명)
            page (str): 페이지명(컬렉션명)

        Example:
            c103손익계산서q (c103손q, c103iq, c103_iq)\n
            c103재무상태표y (c103재q, c103bq, c103_bq)\n
            c103현금흐름표q (c103현q, c103cq, c103_cq)\n

        """
        if page.startswith('c103') and page[-1] in ['q', 'y']:
            if page[4:-1] in ['손익계산서', '손', 'i', '_i']:
                super().__init__(code=code, page=''.join([page[:4], '손익계산서', page[-1]]))
            elif page[4:-1] in ['재무상태표', '재', 'b', '_b']:
                super().__init__(code=code, page=''.join([page[:4], '재무상태표', page[-1]]))
            elif page[4:-1] in ['현금흐름표', '현', 'c', '_c']:
                super().__init__(code=code, page=''.join([page[:4], '현금흐름표', page[-1]]))
            else:
                raise ValueError(f'Invalid value : {page}')
        else:
            raise ValueError(f'Invalid value : {page}')

    def chg_page(self, page: str):
        if page.startswith('c103') and page[-1] in ['q', 'y']:
            if page[4:-1] in ['손익계산서', '손', 'i', '_i']:
                super().chg_page(page=''.join([page[:4], '손익계산서', page[-1]]))
            elif page[4:-1] in ['재무상태표', '재', 'b', '_b']:
                super().chg_page(page=''.join([page[:4], '재무상태표', page[-1]]))
            elif page[4:-1] in ['현금흐름표', '현', 'c', '_c']:
                super().chg_page(page=''.join([page[:4], '현금흐름표', page[-1]]))
            else:
                raise ValueError(f'Invalid value : {page}')
        else:
            raise ValueError(f'Invalid value : {page}')

    def save(self, c103_list: list) -> bool:
        """데이터베이스에 저장

        Args:
            c103_list (list): 딕셔너리를 담은 리스트 형식

        Returns:
            bool: 저장 성공 실패 여부

        Example:
            c103_list 예시\n
            [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
            {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        c103_list.append({'stamp': datetime.datetime.now()})  # c103가 리스트라서 append 사용
        # delete all documents in a collection
        self.client[self.db][self.col].delete_many({})
        result = self.client[self.db][self.col].insert_many(c103_list)
        return result.acknowledged


class Noti(Base):
    def __init__(self):
        super().__init__(db='noti', col='noti')

    def save(self, noti_dict: dict) -> bool:
        """

        Args:
            noti_dict (dict) : dart 에서 전달되는 딕셔너리 구조

        Note:
            noti_dict 구조\n
            {'code': '005930',\n
            'rcept_no': '20210514000624',\n
            'rcept_dt': '20210514',\n
            'report_nm': '임원ㆍ주요주주특정증권등소유상황보고서',\n
            'point': 2,\n
            'text': '등기임원이 1.0억 이상 구매하지 않음.'}\n
        """
        self.client[self.db][self.col].delete_many({'rcept_no': {"$eq": noti_dict['rcept_no']}})
        result = self.client[self.db][self.col].insert_one(noti_dict)
        return result.acknowledged

    def get_data(self) -> DataFrame:
        try:
            df = DataFrame(list(self.client[self.db][self.col].find())).drop(columns=['_id'])
        except KeyError:
            df = DataFrame()
        return df

    def cleaning_data(self, days_ago: int = 15):
        """

        days_ago 인자를 기준으로 이전 날짜의 데이터를 검색하여 삭제한다.
        본 함수를 주기적으로 실행해 준다.
        """
        border_date_str = (datetime.datetime.today() - datetime.timedelta(days=days_ago)).strftime('%Y%m%d')
        try:
            self.client[self.db][self.col].delete_many({'rcept_dt': {'$lt': border_date_str}})
            logger.info(f'Delete noti data before {days_ago} days ago..')
        except:
            logger.error(f'Error occurred while delete noti data..')
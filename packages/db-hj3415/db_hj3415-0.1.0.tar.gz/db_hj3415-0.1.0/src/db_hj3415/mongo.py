import datetime
import math
import re
import pymongo
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


class Base:
    def __init__(self, db, col):
        self.mongo_addr = load_setting()['mongo']

        # mongodb 에 연결
        self.client = pymongo.MongoClient(self.mongo_addr)
        self.db = db
        self.col = col
        logger.info(f"__init__ set db : {self.db}\tcol : {self.col}")

    # ======================Base 만 가지는 함수들 ===========================

    def get_status(self) -> tuple:
        """
        현재 설정된 (db, col)을 반환한다. - ex)('005930', 'c103재무상태표q')
        """
        return self.mongo_addr, self.db, self.col

    def chg_addr(self, addr: str):
        """
        파일에 저장되는 세팅이 바뀌는 것이 아니라 클래스의 설명만 바뀌는 것임
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

    def get_all_db(self) -> list:
        return sorted(self.client.list_database_names())

    def drop_all_db(self):
        pre_db = self.get_all_db()
        for db in pre_db:
            self.client.drop_database(db)
        post_db = self.get_all_db()
        print(f"Drop all db..{len(pre_db)} -> {len(post_db)}")

    def drop_db(self, db: str):
        pre_db = self.get_all_db()
        if db in pre_db:
            self.client.drop_database(db)
            post_db = self.get_all_db()
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
    mongodb에 저장된 market index를 가져오는 클래스
    <<구조>>
    데이터베이스 - mi
    컬렉션 - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx'
    도큐멘트 - date, value
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
        if index == '':
            pass
        else:
            self.chg_index(index=index)

        d = self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
        del d['_id']
        return d

    def save(self, mi_dict: dict, index: str = '') -> bool:
        """
        mi_dict의 구조 - {'date': '2021.07.21', 'value': '1154.50'}
        index 종류 - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx'
        """
        if index != '':
            self.chg_index(index=index)
        self.client[self.db][self.col].delete_many({'date': {"$eq": mi_dict['date']}})
        result = self.client[self.db][self.col].insert_one(mi_dict)
        return result.acknowledged


class Corps(Base):
    """
    mongodb에 저장된 재무데이터를 가져오는 클래스
    <<구조>>
    데이터베이스 - 6자리 코드명
    컬렉션 - c101, c103손익계산서qy, c103재무상태표qy, c103현금흐름표qy, c104qy, c106, c108, dart
    도큐멘트참고
        - c106은 q와 y의 2개의 도큐먼트로 구성
        - c104는 중복되는 항목이 없어 2개의 페이지로 나눔
        - c103는 중복되는 항목이 있어 6개의 페이지로 나눔
    """
    COL_TITLE = ('c101', 'c104y', 'c104q', 'c106', 'c108',
                 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y', 'dart')

    def __init__(self, code: str, page='c101'):
        if utils.is_6digit(code) and page in self.COL_TITLE:
            super().__init__(db=code, col=page)
        else:
            raise ValueError(f'Invalid value : {code}(6 digit) / {page}({self.COL_TITLE})')

    # ======================Corps 만 가지는 함수들 ===========================

    def chg_code(self, code: str):
        # code 가 6자리 숫자인지 확인 후 세팅
        if utils.is_6digit(code):
            logger.info(f'Set db : {self.db} -> {code}')
            self.db = code
        else:
            raise ValueError(f'Invalid value : {code}(6 digit)')

    def chg_page(self, page: str):
        # page 가 COL_TITLE 인지 확인 후 세팅
        if page in self.COL_TITLE:
            logger.info(f'Set col : {self.col} -> {page}')
            self.col = page
        else:
            raise ValueError(f'Invalid col name : {page}({self.COL_TITLE})')

    # ======================부모 클래스에서 재구성한 함수들================

    def get_all_corps(self) -> list:
        return_list = []
        for col in super().get_all_db():
            if utils.is_6digit(col):
                return_list.append(col)
        return sorted(return_list)

    def drop_all_corps(self):
        pre_db = self.get_all_corps()
        for db in pre_db:
            self.client.drop_database(db)
        post_db = self.get_all_corps()
        print(f"Drop all corps..{len(pre_db)} -> {len(post_db)}")

    def drop_corp(self, code: str):
        if utils.is_6digit(code):
            super().drop_db(db=code)
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
        date 입력형식 예 - 20201011(6자리숫자)
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
        items = []
        for doc in self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> dict:
        # 리턴값의 일관성을 위해서 list로 한번 포장한다.
        d = self.client[self.db][self.col].find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
        del d['_id']
        return d


class C108(Corps):
    def __init__(self, code: str):
        super().__init__(code=code, page='c108')

    # ========================특정 페이지 관련 함수들=======================

    def get_all(self) -> list:
        items = []
        for doc in self.client[self.db][self.col].find({'날짜': {'$exists': True}}).sort('날짜', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items

    def get_recent(self) -> list:
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
        - 인자 c108 리스트 형식
        [{'날짜': '21/07/19', '제목': '...', '작성자': '...', '제공처': '...', '투자의견': '...', '목표가': '95,000', '내용': '...'},
        {'날짜': '21/07/12', '제목': '...', '작성자': '김운호', '제공처': 'IBK', '투자의견': '매수', '목표가': '110,000', '내용': '...'},
        """
        c108_list.append({'stamp': datetime.datetime.now()})  # c108가 리스트라서 append 사용
        # delete all documents in a collection
        self.client[self.db][self.col].delete_many({})
        result = self.client[self.db][self.col].insert_many(c108_list)
        return result.acknowledged


class C106(Corps):
    PERIOD = ['q', 'y']

    def __init__(self, code: str, page: str):
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
        - 인자 c106 딕셔너리 형식
        {'전일종가': {'동화약품': '14600', '환인제약': '24700', '큐라클': '24100', '하나제약': '7600', '노바렉스': '27900'},
        '시가총액': {'동화약품': '4078.0', '환인제약': '4039.6', '큐라클': '4260.7', '하나제약': '3811.7', '노바렉스': '4606.6'}}
        - 각 항목이 중복되지 않는 경우라서 항목을 키로하는 딕셔너리를 인자로 받는다.
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
        전년/분기대비 값을 반환하는 함수
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
        return self.get_all()[title]

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
        last_one = od.popitem(last=True)
        if math.isnan(last_one[1]):
            last_one = od.popitem(last=True)
            if last_one is None:
                return None, 0
        return tuple(last_one)


class C104(C1034):
    def __init__(self, code: str, page: str):
        super().__init__(code=code, page=page)

    def save(self, c104_list: list) -> bool:
        """
        - 인자 c103 리스트 형식
         [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
         {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]
        - 항목이 중복되는 경우가 있기 때문에 각 항목을 키로하는 딕셔너리로 만들지 않는다..
        """
        time_now = datetime.datetime.now()
        c104_list.append({'stamp': time_now})  # c104가 리스트라서 append 사용
        # c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에 stamp를 검사하여 12시간전보다 이전에 저장된 자료가 있으면 삭제한 후
        # 저장하고 12시간 이내의 자료는 삭제하지 않고 데이터를 추가하는 형식으로 저장한다.
        if self.client[self.db][self.col].find_one({'stamp': {'$lt': time_now - datetime.timedelta(days=.5)}}):
            self.client[self.db][self.col].delete_many({})  # delete all documents in a collection
        result = self.client[self.db][self.col].insert_many(c104_list)
        return result.acknowledged


class C103(C1034):
    def __init__(self, code: str, page: str):
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
        """
        - 인자 c103 리스트 형식
         [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
         {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]
        - 항목이 중복되는 경우가 있기 때문에 각 항목을 키로하는 딕셔너리로 만들지 않는다..
        """
        c103_list.append({'stamp': datetime.datetime.now()})  # c103가 리스트라서 append 사용
        # delete all documents in a collection
        self.client[self.db][self.col].delete_many({})
        result = self.client[self.db][self.col].insert_many(c103_list)
        return result.acknowledged

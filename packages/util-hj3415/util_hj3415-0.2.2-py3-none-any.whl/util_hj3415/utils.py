import math
import random
import re
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from krx_hj3415 import krx

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


def to_float(s) -> float:
    """
    인자의 예 '1432', '1,432', '23%', 1432
    인자를 실수형으로 변환하고 불가능하면 nan을 리턴한다.
    """
    def is_digit(str):
        # reference from http://seorenn.blogspot.com/2011/04/python-isdigit.html 음수 is_digit()
        try:
            tmp = float(str)
            return True
        except (ValueError, TypeError):
            return False
    logger.debug(f'to_float : {s}')

    if is_digit(s):
        return float(s)
    elif is_digit(str(s).replace(',', '').replace('%', '')):
        return float(s.replace(',', '').replace('%', ''))
    else:
        return float('nan')


def to_int(s):
    t = to_float(s)
    if math.isnan(t):
        return t
    else:
        return int(t)


def deco_num(s):
    # 숫자형 인수를 받아서 천단위에 컴마가 붙은 문자열로 반환한다.
    t = to_int(s)
    return None if s is None or math.isnan(t) else format(t, ",")


def to_억(v) -> str:
    """
    유동형식 인자를 입력받아 float으로 바꿔 nan이면 '-'리턴 아니면 '억'을 포함한 읽기쉬운 숫자 문자열로 반환
    """
    logger.debug(f'to_억 : {v}')
    float_v = to_float(v)
    if math.isnan(float_v):
        return '-'
    else:
        return str(round(float_v / 100000000, 1)) + '억'


def to_만(v) -> str:
    """
    유동형식 인자를 입력받아 float으로 바꿔 nan이면 '-'리턴 아니면 '만'을 포함한 읽기쉬운 숫자 문자열로 반환
    """
    logger.debug(f'to_만 : {v}')
    float_v = to_float(v)
    if math.isnan(float_v):
        return '-'
    else:
        return str(int(float_v / 10000)) + '만'


def str_to_date(d: str) -> datetime.datetime:
    """
    다양한 형태의 날짜 문자열을 날짜형식으로 변환
    '2021년 04월 13일'
    '2021/04/13'
    '2021-04-13'
    '2021.04.13'
    '20210413'
    """
    r = re.compile('^(20[0-9][0-9])[가-힣/.\-]?([0,1][0-9])[가-힣/.\-]?([0-3][0-9])[가-힣/.\-]?$')
    try:
        Ymd = "".join(re.findall(r, d.replace(' ', ''))[0])
    except IndexError:
        # 입력문자열이 날짜형식이 아닌경우 - ex) '-'
        return d
    return datetime.datetime.strptime(Ymd, '%Y%m%d')


def date_to_str(d: datetime.datetime, sep: str = '-') -> str:
    """
    datetime 형식을 %Ysep%msep%d형식으로 반환
    """
    s = d.strftime('%Y%m%d')
    if sep is None:
        return s
    else:
        return s[0:4] + sep + s[4:6] + sep + s[6:8]


def isYmd(date: str) -> bool:
    """
    date 인자의 형식이 Ymd 인지 확인

    Args:
        date (str): 날자 형태의 문자열

    Example:
        True : 20101120
        False : 2010.11.20
    """
    # date 형식여부 확인
    p = re.compile('^20[0-9][0-9][0,1][0-9][0-3][0-9]$')
    if p.match(date) is None:
        return False
    return True


def isY_slash_m(date: str) -> bool:
    """
    date 인자의 형식이 Y/m 인지 확인

    Args:
        date (str): 날자 형태의 문자열

    Example:
        True : 2010/11
        False : 2010.11
    """
    p = re.compile('^20[0-9][0-9]/[0,1][0-9]$')
    if p.match(date) is None:
        return False
    return True


def ext_latest_value(period_dict: dict) -> tuple:
    if len(period_dict) == 0:
        return '', float('nan')
    else:
        return max(period_dict.keys()), float(period_dict[max(period_dict.keys())])


def is_6digit(word: str) -> bool:
    # 파일명이 숫자6자리로 되어있는지 검사하여 참거짓 반환
    p = re.compile('^\d\d\d\d\d\d$')
    m = p.match(word)
    if m:
        return True
    else:
        return False


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'From': 'hj3415@hanmail.net'
}


def scrape_simple_data(url, selector):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    logger.error(soup.select(selector))
    raw_data = soup.select(selector)[0]
    data = re.sub(r'<.+?>', '', str(raw_data).replace('\t', '').replace('\n', ''))
    return data


def get_price_now(code: str) -> tuple:
    """
    code에 해당하는 현재 시세를 조회하여 {'price':...,'updown':...} 딕셔너리 반환한다.
    """
    # 현재 시세를 조회한다.
    url = f"https://finance.naver.com/item/sise_day.nhn?code={code}&page=1"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 현재가 추출
    raw_data = soup.select(f'body > table.type2 > tr:nth-child(3) > td:nth-child(2) > span')
    try:
        현재가 = int(re.sub(r'\<.+?\>', '', str(raw_data).strip('[]').replace('\n', '').replace(',', '')))
    except ValueError:
        logger.error(f'현재가 에러 : {code} -> return 0, 0, None')
        return 0, 0, None

    # 전일비 추출
    raw_data = soup.select(f'body > table.type2 > tr:nth-child(3) > td:nth-child(3) > span')
    try:
        전일비 = int(re.sub(r'\<.+?\>', '', str(raw_data).strip('[]').replace('\n', '').replace(',', '')))
    except ValueError:
        logger.error(f'전일비 에러 : {code} -> return {현재가}, 0, None')
        return 현재가, 0, None

    # 상승, 하락 추출
    try:
        # red02 or nv01
        raw_data = soup.select('body > table.type2 > tr:nth-child(3) > td:nth-child(3) > span')[0]['class'][2]
        if raw_data == 'red02':
            updown = 'up'
        elif raw_data == 'nv01':
            updown = 'down'
        else:
            updown = None
    except IndexError:
        # none인 경우
        updown = None

    return 현재가, 전일비, updown


def get_driver(verbose=False):
    # 크롬드라이버 옵션세팅
    options = webdriver.ChromeOptions()
    # reference from https://gmyankee.tistory.com/240
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument("--disable-extensions")

    # 크롬드라이버 준비
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    if verbose:
        print('Get chrome driver successfully...')
    return driver


codes = list(krx.get_codes())


def pick_rnd_x_code(x: int) -> list:
    """
    인자 x 개 만큼의 랜덤한 종목코드를 추출하여 리스트로 반환한다.
    """
    c = codes
    random.shuffle(c)
    return c[:x]

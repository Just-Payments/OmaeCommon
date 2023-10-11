import json
import logging
import math
import pytz
import random
import requests
import string
from datetime import datetime


# datetime wrapper

def current_aware_time(zone=pytz.utc):
    now = datetime.utcnow()
    if zone == pytz.utc:
        return zone.localize(now)
    else:
        return pytz.utc.localize(now).astimezone(zone)


def change_time_zone(dt: datetime, tzstr='Asia/Seoul'):
    tz = pytz.timezone(tzstr)
    return dt.astimezone(tz)


# 사업자등록번호 검사

def validate_buzno(input: str):
    if len(input) != 10 or input.isnumeric() != True:
        return False
    
    sum = 0
    keys = [1, 3, 7, 1, 3, 7, 1, 3, 5]
    for key, bzno in zip(keys, input):
        sum += (key * int(bzno))

    sum += math.floor((keys[8] * int(input[8])) / 10)
    remainder = sum % 10

    if int(input[9]) == (10 - remainder):
        return True
    elif remainder == 0 and int(input[9]) == 0:
        return True

    return False


# 법인등록번호 검사
def validate_corpno(input: str):
    if len(input) != 13 or input.isnumeric() != True:
        return False
    
    sum = 0
    keys = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    for key, corpno in zip(keys, input):
        sum += (key * int(corpno))

    remainder = sum % 10
    if remainder > 0:
        if int(input[12]) == (10 - remainder):
            return True
    else:
        if int(input[12]) == 0:
            return True
        
    return False


# 공공데이터포털: 사업자 정보 확인
def validate_odcloud(svckey: str, buzNo: str, name: str, owner: str,
                     opendate: str, corp_no: str = ""):
    try:
        url = f'https://api.odcloud.kr/api/nts-businessman/v1/validate?serviceKey={svckey}'

        HEADERS = { 
            'Content-Type': 'application/json',
            'charset': 'utf-8',
            'Accept': 'application/json'
        }

        payload = {
            'businesses': [
                {
                    "b_no": buzNo.replace("-", ""),
                    "start_dt": opendate.replace("-", ""),
                    "p_nm": owner,
                    "p_nm2": "",
                    "b_nm": name,
                    "corp_no": corp_no,
                    "b_sector": "",
                    "b_type": ""
                }
            ]
        }

        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, headers=HEADERS, data=data)
        if response.status_code == 200:
            json_obj = json.loads(response.text)
            if (json_obj["status_code"] == "OK" and "valid_cnt" in json_obj and
                json_obj["valid_cnt"] == json_obj["request_cnt"]):
                return json_obj["data"][0]
            else:
                return None
        else:
            return None
    except:
        return None


# logging wrapper

def info_log(name: str, message: str, tag: str = ''):
    logging.getLogger(name).info(f"{tag}: {message}")


def err_log_with_exception(name: str, message: str, tag: str = ''):
    logging.getLogger(name).exception(f"{tag}: {message}")


# string utilities

def get_random_string(len: int = 8) -> str:
    special = '*#@_!'
    alphanumeric = string.ascii_letters + string.digits + special

    passwd_list = []
    for i in range(0, len):
        passwd_list.append(random.choice(alphanumeric))

    passwd_list.append(random.choice(string.digits))
    passwd_list.append(random.choice(string.ascii_lowercase))
    passwd_list.append(random.choice(string.ascii_uppercase))
    passwd_list.append(random.choice(special))
    
    random.SystemRandom().shuffle(passwd_list)
    return ''.join(passwd_list)
import math
import pytz
from datetime import datetime


def current_aware_time(zone=pytz.utc):
    return zone.localize(datetime.utcnow())


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

    return False
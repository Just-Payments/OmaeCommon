import pytz
from datetime import datetime

def current_aware_time(zone=pytz.utc):
    return zone.localize(datetime.utcnow())
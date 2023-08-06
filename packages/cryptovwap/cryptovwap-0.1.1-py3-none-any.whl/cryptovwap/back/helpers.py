from datetime import datetime as dt
from dateutil.parser import isoparse


def dt_unix_datetime(unix):
    return dt.fromtimestamp(unix)


def dt_datetime_unix(date):
    return date.timestamp()


def dt_str_datetime(date):
    return isoparse(date)


def generate_filter(date, interval_filter):
    return int(date / interval_filter) * interval_filter


FREQ_VWAP = {
    "1 min": 60,
    "5 min": 60*5,
    "30 min": 60*30,
    "1 h": 60*60
}
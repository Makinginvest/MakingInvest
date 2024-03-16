import datetime

import numpy as np
import pandas as pd


def get_now_floor(period="15min"):
    _period = period
    if period == "5m":
        _period = "5min"
    if period == "15m":
        _period = "15min"
    if period == "30m":
        _period = "30min"

    now = datetime.datetime.utcnow()
    now_5m = now - datetime.timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)
    now_5m = np.datetime64(now_5m)
    now_5m = pd.to_datetime(now_5m, utc=True)

    now_15m = now - datetime.timedelta(minutes=now.minute % 15, seconds=now.second, microseconds=now.microsecond)
    now_15m = np.datetime64(now_15m)
    now_15m = pd.to_datetime(now_15m, utc=True)

    now_30m = now - datetime.timedelta(minutes=now.minute % 30, seconds=now.second, microseconds=now.microsecond)
    now_30m = np.datetime64(now_30m)
    now_30m = pd.to_datetime(now_30m, utc=True)

    # floor to 1 hour
    now_1hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_1hr = np.datetime64(now_1hr)
    now_1hr = pd.to_datetime(now_1hr, utc=True)

    now_2hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_2hr = now_2hr - datetime.timedelta(hours=now_2hr.hour % 2)
    now_2hr = np.datetime64(now_2hr)
    now_2hr = pd.to_datetime(now_2hr, utc=True)

    now_4hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_4hr = now_4hr - datetime.timedelta(hours=now_4hr.hour % 4)
    now_4hr = np.datetime64(now_4hr)
    now_4hr = pd.to_datetime(now_4hr, utc=True)

    now_6hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_6hr = now_6hr - datetime.timedelta(hours=now_6hr.hour % 6)
    now_6hr = np.datetime64(now_6hr)
    now_6hr = pd.to_datetime(now_6hr, utc=True)

    now_8hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_8hr = now_8hr - datetime.timedelta(hours=now_8hr.hour % 8)
    now_8hr = np.datetime64(now_8hr)
    now_8hr = pd.to_datetime(now_8hr, utc=True)

    now_12hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_12hr = now_12hr - datetime.timedelta(hours=now_12hr.hour % 12)
    now_12hr = np.datetime64(now_12hr)
    now_12hr = pd.to_datetime(now_12hr, utc=True)

    now_1d = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_1d = now_1d - datetime.timedelta(hours=now_1d.hour)
    now_1d = np.datetime64(now_1d)
    now_1d = pd.to_datetime(now_1d, utc=True)

    if _period == "5min":
        return now_5m
    elif _period == "15min":
        return now_15m
    elif _period == "30min":
        return now_30m
    elif _period == "1h":
        return now_1hr
    elif _period == "2h":
        return now_2hr
    elif _period == "4h":
        return now_4hr
    elif _period == "6h":
        return now_6hr
    elif _period == "8h":
        return now_8hr

    elif _period == "12h":
        return now_12hr
    elif _period == "1d":
        return now_1d
    else:
        return None

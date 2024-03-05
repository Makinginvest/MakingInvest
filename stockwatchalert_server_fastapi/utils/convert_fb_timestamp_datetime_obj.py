from datetime import datetime
import numpy as np
import pandas as pd
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def check_fb_timestamp_datetime_obj(obj):
    """Check if object any value in object has DatetimeWithNanoseconds type and convert to datetime."""
    for key, value in obj.items():
        if isinstance(value, DatetimeWithNanoseconds):
            year, month, day, hour, minute, second, tzinfo = value.year, value.month, value.day, value.hour, value.minute, value.second, value.tzinfo
            val = datetime(year, month, day, hour, minute, second, tzinfo=tzinfo)
            obj[key] = val

    return obj

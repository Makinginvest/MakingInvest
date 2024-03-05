import pandas as pd


def get_validate_generate_signals_4h_6h(useOldSignal: bool = True, factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor_4h = date_now_utc.floor("4h")
    data_now_utc_floor_6h = date_now_utc.floor("6h")
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor_4h).seconds < factor * 60:
            return True
        if (date_now_utc - data_now_utc_floor_6h).seconds < factor * 60:
            return True

    return False


def get_validate_generate_signals(useOldSignal: bool = True, floor="6h", floor_factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor = date_now_utc.floor(floor)
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor).seconds < floor_factor * 60:
            return True

    return False


def get_validate_generate_signals_4h(useOldSignal: bool = True, factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor_4h = date_now_utc.floor("4h")
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor_4h).seconds < factor * 60:
            return True

    return False


def get_validate_generate_signals_2h(useOldSignal: bool = True, factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor_2h = date_now_utc.floor("2h")
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor_2h).seconds < factor * 60:
            return True

    return False


def get_validate_generate_signals_1h(useOldSignal: bool = True, factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor_1h = date_now_utc.floor("1h")
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor_1h).seconds < factor * 60:
            return True

    return False


def get_validate_generate_signals_30m(useOldSignal: bool = True, factor: int = 15):
    if useOldSignal == False:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor_30m = date_now_utc.floor("30min")
    if useOldSignal:
        if (date_now_utc - data_now_utc_floor_30m).seconds < factor * 60:
            return True

    return False

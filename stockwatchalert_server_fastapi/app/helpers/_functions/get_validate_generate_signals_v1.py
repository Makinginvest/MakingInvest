import pandas as pd


def get_validate_generate_signals_v1(use_old_signal: bool = True, floor="4h", floor_factor: int = 15, force_gen_new_signals: bool = True):
    if use_old_signal == False:
        return True

    if force_gen_new_signals == True:
        return True

    date_now_utc = pd.Timestamp.utcnow()
    data_now_utc_floor = date_now_utc.floor(floor)
    if use_old_signal:
        if (date_now_utc - data_now_utc_floor).seconds < floor_factor * 60:
            return True

    return False

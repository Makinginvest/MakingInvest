import pandas as pd
import pandas_ta as ta


def smoothed_ha_candles(close: pd.Series = None, open_: pd.Series = None, high: pd.Series = None, low: pd.Series = None, length: int = 10, length2: int = 10):
    # Define variables
    open_ema = ta.ema(open_, length=length)
    close_ema = ta.ema(close, length=length)
    high_ema = ta.ema(high, length=length)
    low_ema = ta.ema(low, length=length)

    ha_close = (open_ema + high_ema + low_ema + close_ema) / 4
    ha_open = ta.sma(ha_close, length=length).shift(1).combine_first((open_ + close) / 2)
    ha_high = pd.concat(
        [
            high,
            ha_open,
            ha_close,
        ],
        axis=1,
    ).max(axis=1)
    ha_low = pd.concat(
        [
            low,
            ha_open,
            ha_close,
        ],
        axis=1,
    ).min(axis=1)

    ha_open_ema = ta.ema(ha_open, length=length2)
    ha_close_ema = ta.ema(ha_close, length=length2)
    ha_high_ema = ta.ema(ha_high, length=length2)
    ha_low_ema = ta.ema(ha_low, length=length2)

    return {
        "ha_open_ema": ha_open_ema,
        "ha_close_ema": ha_close_ema,
        "ha_high_ema": ha_high_ema,
        "ha_low_ema": ha_low_ema,
    }

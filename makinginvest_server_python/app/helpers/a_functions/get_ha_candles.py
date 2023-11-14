import pandas_ta as pta


def get_ha_candles(df):
    _df = df.copy()
    ha = pta.ha(open_=_df["open"], high=_df["high"], low=_df["low"], close=_df["close"])
    _df["ha_open"] = ha["HA_open"]
    _df["ha_high"] = ha["HA_high"]
    _df["ha_low"] = ha["HA_low"]
    _df["ha_close"] = ha["HA_close"]
    columns = ["ha_open", "ha_high", "ha_low", "ha_close"]
    return _df[columns]

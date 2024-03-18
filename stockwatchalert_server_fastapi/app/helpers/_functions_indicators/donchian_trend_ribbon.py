def donchian_trend_ribbon(close, dlen):
    hh = close.rolling(window=dlen).max()
    ll = close.rolling(window=dlen).min()

    trend = (close > hh.shift(1)).astype(int) - (close < ll.shift(1)).astype(int)
    trend = trend.replace(0, method="ffill")

    return trend

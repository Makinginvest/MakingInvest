import pandas as pd


def get_resample_df(_df: pd.DataFrame, timeframe="15m"):
    _timeframe = timeframe
    if timeframe == "30m":
        _timeframe = "30min"

    if timeframe == "15m":
        _timeframe = "15min"

    df = _df.resample(_timeframe).agg(
        {
            "close": "last",
            "high": "max",
            "low": "min",
            "volume": "sum",
            "open": "first",
            "dateTimeUtc": "first",
            "dateTimeEst": "first",
            "symbol": "first",
            "timeframe": "first",
        }
    )
    df["timeframe"] = timeframe

    # remove time not multiple of 5 mins
    if timeframe == "5m":
        df = df[df["dateTimeUtc"].dt.minute % 5 == 0]

    # remove time not multiple of 15 mins
    if timeframe == "15m":
        df = df[df["dateTimeUtc"].dt.minute % 15 == 0]

    # remove time not multiple of 30 mins
    if timeframe == "30m":
        df = df[df["dateTimeUtc"].dt.minute % 30 == 0]

    # remove time not multiple of 1 hour
    if timeframe == "1h":
        df = df[df["dateTimeUtc"].dt.hour % 1 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 2 hours
    if timeframe == "2h":
        df = df[df["dateTimeUtc"].dt.hour % 2 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 4 hours
    if timeframe == "4h":
        df = df[df["dateTimeUtc"].dt.hour % 4 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 6 hours
    if timeframe == "6h":
        df = df[df["dateTimeUtc"].dt.hour % 6 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 8 hours
    if timeframe == "8h":
        df = df[df["dateTimeUtc"].dt.hour % 8 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 12 hours
    if timeframe == "12h":
        df = df[df["dateTimeUtc"].dt.hour % 12 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    # remove time not multiple of 1 day
    if timeframe == "1d":
        df = df[df["dateTimeUtc"].dt.hour % 24 == 0]
        df = df[df["dateTimeUtc"].dt.minute % 60 == 0]

    return df

import numpy as np
import pandas as pd


def get_supertrend_df(df, atr_period, multiplier):

    high = df["high"]
    low = df["low"]
    close = df["close"]

    # calculate ATR
    price_diffs = [
        high - low,
        high - close.shift(),
        close.shift() - low,
    ]

    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1 / atr_period, min_periods=atr_period).mean()

    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2
    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    # initialize Supertrend column to True
    supertrend = [True] * len(df)

    for i in range(1, len(df.index)):
        (curr, prev) = (i, i - 1)

        # if current close price crosses above upperband
        if close[curr] > upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]

            # adjustment to the final bands
            if supertrend[curr] == True and lowerband[curr] < lowerband[prev]:
                lowerband[curr] = lowerband[prev]
            if supertrend[curr] == False and upperband[curr] > upperband[prev]:
                upperband[curr] = upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            upperband[curr] = np.nan
        else:
            lowerband[curr] = np.nan

    return pd.DataFrame(
        {
            "Supertrend": supertrend,
            "Final Lowerband": lowerband,
            "Final Upperband": upperband,
        },
        index=df.index,
    )

import pandas as pd


def get_take_profit_pct(df: pd.DataFrame = None, pct1: float = None, pct2: float = None, pct3: float = None, pct4: float = None, is_heiken_ashi: bool = False):

    if pct4 != None:
        return get_take_profit_pct_periods4(df, pct1, pct2, pct3, pct4, is_heiken_ashi)
    else:
        return get_take_profit_pct_periods3(df, pct1, pct2, pct3, is_heiken_ashi)


def get_take_profit_pct_periods4(df, pct1, pct2, pct3, pct4, is_heiken_ashi=False):
    signal = df["entryType"]
    close = df["close"] if not is_heiken_ashi else df["r_close"]

    takeProfit1 = []
    takeProfit2 = []
    takeProfit3 = []
    takeProfit4 = []
    takeProfit1Pct = []
    takeProfit2Pct = []
    takeProfit3Pct = []
    takeProfit4Pct = []
    takeProfit1Pips = []
    takeProfit2Pips = []
    takeProfit3Pips = []
    takeProfit4Pips = []
    for i in range(len(signal)):
        if signal[i] == "long":
            takeProfit4.append(close[i] * (1 + pct4))
            takeProfit3.append(close[i] * (1 + pct3))
            takeProfit2.append(close[i] * (1 + pct2))
            takeProfit1.append(close[i] * (1 + pct1))

            takeProfit4Pct.append(pct4)
            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit4Pips.append((close[i] * (1 + pct4) - close[i]) / 0.0001)
            takeProfit3Pips.append((close[i] * (1 + pct3) - close[i]) / 0.0001)
            takeProfit2Pips.append((close[i] * (1 + pct2) - close[i]) / 0.0001)
            takeProfit1Pips.append((close[i] * (1 + pct1) - close[i]) / 0.0001)

        elif signal[i] == "short":
            takeProfit4.append(close[i] * (1 - pct4))
            takeProfit3.append(close[i] * (1 - pct3))
            takeProfit2.append(close[i] * (1 - pct2))
            takeProfit1.append(close[i] * (1 - pct1))

            takeProfit4Pct.append(pct4)
            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit4Pips.append((close[i] - close[i] * (1 - pct4)) / 0.0001)
            takeProfit3Pips.append((close[i] - close[i] * (1 - pct3)) / 0.0001)
            takeProfit2Pips.append((close[i] - close[i] * (1 - pct2)) / 0.0001)
            takeProfit1Pips.append((close[i] - close[i] * (1 - pct1)) / 0.0001)

        else:
            takeProfit4.append(0)
            takeProfit3.append(0)
            takeProfit2.append(0)
            takeProfit1.append(0)

            takeProfit4Pct.append(0)
            takeProfit3Pct.append(0)
            takeProfit2Pct.append(0)
            takeProfit1Pct.append(0)

            takeProfit4Pips.append(0)
            takeProfit3Pips.append(0)
            takeProfit2Pips.append(0)
            takeProfit1Pips.append(0)

    # create new dataframe

    df = pd.DataFrame(
        {
            "takeProfit1": takeProfit1,
            "takeProfit2": takeProfit2,
            "takeProfit3": takeProfit3,
            "takeProfit4": takeProfit4,
            "takeProfit1Pct": takeProfit1Pct,
            "takeProfit2Pct": takeProfit2Pct,
            "takeProfit3Pct": takeProfit3Pct,
            "takeProfit4Pct": takeProfit4Pct,
            "takeProfit1Pips": takeProfit1Pips,
            "takeProfit2Pips": takeProfit2Pips,
            "takeProfit3Pips": takeProfit3Pips,
            "takeProfit4Pips": takeProfit4Pips,
        },
        index=df.index,
    )

    return df


def get_take_profit_pct_periods3(df, pct1, pct2, pct3, is_heiken_ashi=False):
    signal = df["entryType"]
    close = df["close"] if not is_heiken_ashi else df["r_close"]

    takeProfit1 = []
    takeProfit2 = []
    takeProfit3 = []
    takeProfit1Pct = []
    takeProfit2Pct = []
    takeProfit3Pct = []
    takeProfit1Pips = []
    takeProfit2Pips = []
    takeProfit3Pips = []

    for i in range(len(signal)):
        if signal[i] == "long":
            takeProfit3.append(close[i] * (1 + pct3))
            takeProfit2.append(close[i] * (1 + pct2))
            takeProfit1.append(close[i] * (1 + pct1))

            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit1Pips.append((close[i] * (1 + pct1) - close[i]) / 0.0001)
            takeProfit2Pips.append((close[i] * (1 + pct2) - close[i]) / 0.0001)
            takeProfit3Pips.append((close[i] * (1 + pct3) - close[i]) / 0.0001)

        elif signal[i] == "short":
            takeProfit3.append(close[i] * (1 - pct3))
            takeProfit2.append(close[i] * (1 - pct2))
            takeProfit1.append(close[i] * (1 - pct1))

            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit1Pips.append((close[i] - close[i] * (1 - pct1)) / 0.0001)
            takeProfit2Pips.append((close[i] - close[i] * (1 - pct2)) / 0.0001)
            takeProfit3Pips.append((close[i] - close[i] * (1 - pct3)) / 0.0001)

        else:
            takeProfit3.append(0)
            takeProfit2.append(0)
            takeProfit1.append(0)

            takeProfit3Pct.append(0)
            takeProfit2Pct.append(0)
            takeProfit1Pct.append(0)

            takeProfit1Pips.append(0)
            takeProfit2Pips.append(0)
            takeProfit3Pips.append(0)

    # create new dataframe
    df = pd.DataFrame(
        {
            "takeProfit1": takeProfit1,
            "takeProfit2": takeProfit2,
            "takeProfit3": takeProfit3,
            "takeProfit1Pct": takeProfit1Pct,
            "takeProfit2Pct": takeProfit2Pct,
            "takeProfit3Pct": takeProfit3Pct,
            "takeProfit1Pips": takeProfit1Pips,
            "takeProfit2Pips": takeProfit2Pips,
            "takeProfit3Pips": takeProfit3Pips,
        },
        index=df.index,
    )

    return df

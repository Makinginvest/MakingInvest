import pandas as pd


def get_take_profit_atr(df: pd.DataFrame = None, factor1: float = None, factor2: float = None, factor3: float = None, factor4: float = None):

    if factor4 != None:
        return get_take_profit_atr_periods4(df, factor1=factor1, factor2=factor2, factor3=factor3, factor4=factor4)
    else:
        return get_take_profit_atr_periods3(df, factor1=factor1, factor2=factor2, factor3=factor3)


def get_take_profit_atr_periods4(df, factor1=1, factor2=2, factor3=4, factor4=8):
    signal = df["entryType"]
    atr = df["atr"]
    close = df["close"]

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
            takeProfit4.append(close[i] + atr[i] * factor4)
            takeProfit3.append(close[i] + atr[i] * factor3)
            takeProfit2.append(close[i] + atr[i] * factor2)
            takeProfit1.append(close[i] + atr[i] * factor1)

            pct4 = atr[i] * factor4 / close[i]
            pct3 = atr[i] * factor3 / close[i]
            pct2 = atr[i] * factor2 / close[i]
            pct1 = atr[i] * factor1 / close[i]

            takeProfit4Pct.append(pct4)
            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit4Pips.append(pct4 * close[i] * 10000)
            takeProfit3Pips.append(pct3 * close[i] * 10000)
            takeProfit2Pips.append(pct2 * close[i] * 10000)
            takeProfit1Pips.append(pct1 * close[i] * 10000)

        elif signal[i] == "short":
            takeProfit4.append(close[i] - atr[i] * factor4)
            takeProfit3.append(close[i] - atr[i] * factor3)
            takeProfit2.append(close[i] - atr[i] * factor2)
            takeProfit1.append(close[i] - atr[i] * factor1)

            pct4 = atr[i] * factor4 / close[i]
            pct3 = atr[i] * factor3 / close[i]
            pct2 = atr[i] * factor2 / close[i]
            pct1 = atr[i] * factor1 / close[i]

            takeProfit4Pct.append(pct4)
            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit4Pips.append(pct4 * close[i] * 10000)
            takeProfit3Pips.append(pct3 * close[i] * 10000)
            takeProfit2Pips.append(pct2 * close[i] * 10000)
            takeProfit1Pips.append(pct1 * close[i] * 10000)

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
            "takeProfit1Pct": takeProfit1Pct,
            "takeProfit2": takeProfit2,
            "takeProfit2Pct": takeProfit2Pct,
            "takeProfit3": takeProfit3,
            "takeProfit3Pct": takeProfit3Pct,
            "takeProfit4": takeProfit4,
            "takeProfit4Pct": takeProfit4Pct,
            "takeProfit1Pips": takeProfit1Pips,
            "takeProfit2Pips": takeProfit2Pips,
            "takeProfit3Pips": takeProfit3Pips,
            "takeProfit4Pips": takeProfit4Pips,
        },
        index=df.index,
    )

    return df


def get_take_profit_atr_periods3(df, factor1=1, factor2=2, factor3=4):
    signal = df["entryType"]
    atr = df["atr"]
    close = df["close"]

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
            takeProfit3.append(close[i] + atr[i] * factor3)
            takeProfit2.append(close[i] + atr[i] * factor3)
            takeProfit1.append(close[i] + atr[i] * factor1)

            pct3 = atr[i] * factor3 / close[i]
            pct2 = atr[i] * factor2 / close[i]
            pct1 = atr[i] * factor1 / close[i]

            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit3Pips.append(pct3 * close[i] * 10000)
            takeProfit2Pips.append(pct2 * close[i] * 10000)
            takeProfit1Pips.append(pct1 * close[i] * 10000)

        elif signal[i] == "short":
            takeProfit3.append(close[i] - atr[i] * factor3)
            takeProfit2.append(close[i] - atr[i] * factor3)
            takeProfit1.append(close[i] - atr[i] * factor1)

            pct3 = atr[i] * factor3 / close[i]
            pct2 = atr[i] * factor2 / close[i]
            pct1 = atr[i] * factor1 / close[i]

            takeProfit3Pct.append(pct3)
            takeProfit2Pct.append(pct2)
            takeProfit1Pct.append(pct1)

            takeProfit3Pips.append(pct3 * close[i] * 10000)
            takeProfit2Pips.append(pct2 * close[i] * 10000)
            takeProfit1Pips.append(pct1 * close[i] * 10000)

        else:

            takeProfit3.append(0)
            takeProfit2.append(0)
            takeProfit1.append(0)

            takeProfit3Pct.append(0)
            takeProfit2Pct.append(0)
            takeProfit1Pct.append(0)

            takeProfit3Pips.append(0)
            takeProfit2Pips.append(0)
            takeProfit1Pips.append(0)

    # create new dataframe
    df = pd.DataFrame(
        {
            "takeProfit1": takeProfit1,
            "takeProfit1Pct": takeProfit1Pct,
            "takeProfit2": takeProfit2,
            "takeProfit2Pct": takeProfit2Pct,
            "takeProfit3": takeProfit3,
            "takeProfit3Pct": takeProfit3Pct,
            "takeProfit1Pips": takeProfit1Pips,
            "takeProfit2Pips": takeProfit2Pips,
            "takeProfit3Pips": takeProfit3Pips,
        },
        index=df.index,
    )

    return df

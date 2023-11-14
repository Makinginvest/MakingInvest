import pandas as pd


def get_stop_loss_atr(df, factor=1.5):
    signal = df["entryType"]
    atr = df["atr"]
    close = df["close"]

    stopLoss = []
    stopLossPct = []
    stopLossPips = []

    for i in range(len(signal)):
        if signal[i] == "long":
            stopLoss.append(close[i] - atr[i] * factor)
            stopLossPct.append(atr[i] * factor / close[i])

            pct = atr[i] * factor / close[i]
            stopLossPips.append(pct * close[i] * 10000)
        elif signal[i] == "short":
            stopLoss.append(close[i] + atr[i] * factor)

            stopLossPct.append(atr[i] * factor / close[i])
            pct = atr[i] * factor / close[i]
            stopLossPips.append(pct * close[i] * 10000)
        else:
            stopLoss.append(0)
            stopLossPct.append(0)
            stopLossPips.append(0)

    df = pd.DataFrame(
        {
            "stopLoss": stopLoss,
            "stopLossPct": stopLossPct,
            "stopLossPips": stopLossPips,
        },
        index=df.index,
    )

    return df


def get_stop_loss_pct(df, pct=0.06, is_heiken_ashi=False):
    signal = df["entryType"]
    close = df["close"] if not is_heiken_ashi else df["r_close"]

    stopLoss = []
    stopLossPct = []
    stopLossPips = []

    for i in range(len(signal)):
        if signal[i] == "long":
            stopLoss.append(close[i] * (1 - pct))
            stopLossPct.append(pct)
            stopLossPips.append(pct * close[i] * 10000)
        elif signal[i] == "short":
            stopLoss.append(close[i] * (1 + pct))
            stopLossPct.append(pct)
            stopLossPips.append(pct * close[i] * 10000)
        else:
            stopLoss.append(0)
            stopLossPct.append(0)
            stopLossPips.append(0)

    df = pd.DataFrame(
        {
            "stopLoss": stopLoss,
            "stopLossPct": stopLossPct,
            "stopLossPips": stopLossPips,
        },
        index=df.index,
    )

    return df


def get_stop_loss_pips(df, pips=30):
    signal = df["entryType"]
    atr = df["atr"]
    close = df["close"]

    stopLoss = []
    stopLossPct = []

    for i in range(len(signal)):
        if signal[i] == "long":
            stopLoss.append(close[i] - pips * 0.0001)
            stopLossPct.append(pips * 0.0001 / close[i])
        elif signal[i] == "short":
            stopLoss.append(close[i] + pips * 0.0001)
            stopLossPct.append(pips * 0.0001 / close[i])
        else:
            stopLoss.append(0)
            stopLossPct.append(0)

    df = pd.DataFrame(
        {
            "stopLoss": stopLoss,
            "stopLossPct": stopLossPct,
        },
        index=df.index,
    )

    return df

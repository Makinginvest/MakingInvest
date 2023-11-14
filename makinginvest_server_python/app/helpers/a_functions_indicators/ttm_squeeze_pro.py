import pandas as pd
import pandas_ta as ta
import numpy as np
from typing import Tuple


def beardy_squeeze_pro(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.DataFrame:
    if not isinstance(high, pd.Series) or not isinstance(low, pd.Series) or not isinstance(close, pd.Series):
        raise ValueError("High, Low, and Close should be pandas Series objects.")
    if length < 1 or not isinstance(length, int):
        raise ValueError("Length should be an integer greater than or equal to 1.")

    data = pd.DataFrame({"High": high, "Low": low, "Close": close})

    # Bollinger Bands
    BB_mult = 2.0
    BB_basis = ta.sma(data["Close"], length)
    dev = BB_mult * ta.stdev(data["Close"], length)
    BB_upper = BB_basis + dev
    BB_lower = BB_basis - dev

    # Keltner Channels
    KC_mult_high = 1.0
    KC_mult_mid = 1.5
    KC_mult_low = 2.0
    KC_basis = ta.sma(data["Close"], length)
    devKC = ta.sma(ta.true_range(data["High"], data["Low"], data["Close"]), length)
    KC_upper_high = KC_basis + devKC * KC_mult_high
    KC_lower_high = KC_basis - devKC * KC_mult_high
    KC_upper_mid = KC_basis + devKC * KC_mult_mid
    KC_lower_mid = KC_basis - devKC * KC_mult_mid
    KC_upper_low = KC_basis + devKC * KC_mult_low
    KC_lower_low = KC_basis - devKC * KC_mult_low

    # Squeeze Conditions
    NoSqz = (BB_lower < KC_lower_low) | (BB_upper > KC_upper_low)
    LowSqz = (BB_lower >= KC_lower_low) | (BB_upper <= KC_upper_low)
    MidSqz = (BB_lower >= KC_lower_mid) | (BB_upper <= KC_upper_mid)
    HighSqz = (BB_lower >= KC_lower_high) | (BB_upper <= KC_upper_high)

    # Momentum Oscillator
    highest_high = data["High"].rolling(window=length).max()
    lowest_low = data["Low"].rolling(window=length).min()
    mom = ta.linreg(data["Close"] - np.mean(np.vstack([highest_high, lowest_low]), axis=0), length)

    # Momentum
    mom_val = np.where(mom > 0, 1, -1)

    # Momentum Histogram Color
    mom_color_val = np.where(mom > np.roll(mom, 1), 1, -1)

    # Squeeze Dots Color
    sq_color_val = np.where(HighSqz, 2, np.where(MidSqz, 1, np.where(LowSqz, 0, -1)))

    # Add the calculated columns to the dataframe
    data["mom"] = mom
    data["mom_color"] = mom_color_val
    data["sq_color"] = sq_color_val

    return data

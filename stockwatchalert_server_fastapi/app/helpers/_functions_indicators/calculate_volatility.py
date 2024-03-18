import numpy as np
import pandas as pd
from pandas import Series


def calculate_volatility(close: Series, lookback: int) -> pd.Series:
    """
    Calculate rolling volatility of a time series.
    :param close: Series with close prices
    :param lookback_days: Lookback period for volatility calculation
    :return: Series of volatility values
    """
    # Calculate daily returns
    returns = np.log(close / close.shift(1))
    returns.fillna(0, inplace=True)

    # Calculate rolling volatility
    volatility_series = returns.rolling(window=lookback).std() * np.sqrt(lookback)

    return volatility_series

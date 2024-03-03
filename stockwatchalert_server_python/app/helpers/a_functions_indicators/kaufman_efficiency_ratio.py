import pandas as pd


def kaufman_efficiency_ratio(close, length=10, directional=False):
    if not isinstance(close, pd.Series):
        raise ValueError("close_prices must be a pandas Series")

    if length < 1:
        raise ValueError("period must be greater than or equal to 1")

    # Calculate the absolute price change over the given period
    price_change = close.diff(length) if directional else close.diff(length).abs()

    # Calculate the absolute daily price changes and their sum over the given period
    daily_price_changes = close.diff().abs()
    cumulative_price_changes = daily_price_changes.rolling(window=length).sum()

    # Calculate the Kaufman Efficiency Ratio
    efficiency_ratio = price_change / cumulative_price_changes

    return efficiency_ratio

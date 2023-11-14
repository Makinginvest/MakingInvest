import numpy as np
import pandas as pd


def check_pct_exceeded(pct, high_low_pct, lookback=14):
    # Create a rolling window of 14 (previous 14 rows) on high_low_pct
    high_low_pct_rolling = high_low_pct.rolling(window=lookback)

    # Calculate the maximum value of high_low_pct within each rolling window
    max_high_low_pct_rolling = high_low_pct_rolling.max()

    # Compare pct with the maximum value in each rolling window, returning 1 if not exceeded, 0 otherwise
    result = np.where(pct > max_high_low_pct_rolling, 1, 0)

    # Set the first 14 values to 0, as there's not enough data for comparison
    result[:lookback] = 0

    # Convert the result array back to a pandas Series with matching index
    result_series = pd.Series(result, index=pct.index)

    return result_series
